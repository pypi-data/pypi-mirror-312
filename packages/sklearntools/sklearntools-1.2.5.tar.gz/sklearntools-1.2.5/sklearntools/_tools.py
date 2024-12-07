import os
import time
from typing import Union
import numpy as np
from collections import Counter
from concurrent.futures import as_completed, ProcessPoolExecutor
from sklearn.model_selection import ParameterGrid
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, mean_squared_error, root_mean_squared_error, mean_absolute_error, r2_score
from logging import basicConfig, INFO, getLogger

logger = getLogger(__name__)
basicConfig(level=INFO, format='[%(asctime)s %(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')


def _log(score, describe, evaluate_fn, is_classifier, cost_time):
	if is_classifier:
		if cost_time:
			print(f'{describe}: {score:.1%} \t 耗时: {cost_time:.2f} seconds.')
		else:
			print(f'{describe}: {score:.1%}')
	else:
		if '准确率' == describe:
			if evaluate_fn == mean_squared_error:
				describe = 'MSE'
			elif evaluate_fn == root_mean_squared_error:
				describe = 'RMSE'
			else:
				describe = 'R2_SCORE'
		if cost_time:
			print(f'{describe}: {score:.2f} \t 耗时: {cost_time:.2f} seconds.')
		else:
			print(f'{describe}: {score:.2f}')
		

def train_evaluate(model, X_train, y_train, X_test, y_test, describe='准确率', verbose=True, return_predict=False,
                   evaluate_fn=None, show_time=False) -> Union[float, tuple[float, list]]:
	"""Train and evaluate a model
	
    Classifier defualt score: accuracy_score
    Regression defualt score: r2_score

	Parameters
    ----------
	model: Model
	X_train:
	y_train:
	X_test:
	y_test:
	verbose:
	describe:
	return_predict: whether return predictions
	evaluate_fn: accuracy_score, mean_squared_error, root_mean_squared_error etc.

	Returns
    -------
    score or (score, predictions)

    Examples
    --------
    >>> import numpy as np
    >>> from sklearn.ensemble import RandomForestClassifier
    >>> from sklearn.model_selection import train_test_split
    >>> from sklearntools import train_evaluate
    >>> X, y = np.arange(20).reshape((10, 2)), range(10)
    >>> X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
    >>> model = RandomForestClassifier(n_estimators=837, bootstrap=False)
    >>> train_evaluate(model, X_train, y_train, X_test, y_test)
    0.88
	"""
	if show_time:
		start_time = time.perf_counter()
		model.fit(X_train, y_train)
		cost_time = time.perf_counter() - start_time
	else:
		cost_time = None
		model.fit(X_train, y_train)
	is_classifier = 'classifier' == model._estimator_type
	if return_predict or evaluate_fn is not None:
		prediction = model.predict(X_test)
		if is_classifier:
			evaluate_fn = evaluate_fn or accuracy_score
		else:
			evaluate_fn = evaluate_fn or r2_score
		if isinstance(evaluate_fn, str):
			fn_dict = {
				"accuracy_score": accuracy_score,
				"acc": accuracy_score,
				"accuracy": accuracy_score,
				"mean_squared_error": mean_squared_error,
				"mse": mean_squared_error,
				"root_mean_squared_error": root_mean_squared_error,
				"rmse": root_mean_squared_error,
				"mean_absolute_error": mean_absolute_error,
				"mae": mean_absolute_error,
				"r2_score": r2_score,
				"r2": r2_score,
			}
			evaluate_fn = evaluate_fn.lower()
			assert evaluate_fn in fn_dict
			evaluate_fn = fn_dict[evaluate_fn]
			
		score = evaluate_fn(y_test, prediction)
		if verbose:
			_log(score, describe, evaluate_fn, is_classifier, cost_time)
		return score, prediction
	else:
		score = model.score(X_test, y_test)
		if verbose:
			_log(score, describe, None, is_classifier, cost_time)
		return score
	

def train_evaluate_split(model, X, y, test_size=0.2, describe='准确率', verbose=True, return_predict=False,
                         random_state=42, evaluate_fn=None, show_time=False) -> Union[float, tuple[float, list]]:
	"""Train and evaluate a model
	
	Classifier defualt score: accuracy_score
    Regression defualt score: r2_score

	Parameters
	----------
	model: Model
	X:
	y:
	test_size:
	verbose:
	describe:
	return_predict: whether return predictions
	random_state:
	evaluate_fn: accuracy_score, mean_squared_error, root_mean_squared_error etc.

	Returns
	-------
	score or (score, predictions)

	Examples
	--------
	>>> import numpy as np
	>>> from sklearn.ensemble import RandomForestClassifier
	>>> from sklearntools import train_evaluate_split
	>>> X, y = np.arange(20).reshape((10, 2)), range(10)
	>>> model = RandomForestClassifier(n_estimators=837, bootstrap=False)
	>>> train_evaluate_split(model, X, y, test_size=0.2)
	0.88
	"""
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
	return train_evaluate(model, X_train, y_train, X_test, y_test, describe, verbose, return_predict, evaluate_fn, show_time)


def search_model_params(model_name, X_train, y_train, X_test, y_test, param_grid, result_num=5, iter_num=8,
                        n_proc: int = None, executor: ProcessPoolExecutor = None, verbose=False) -> list[dict]:
	"""
	Train and evaluate a model

	Parameters
	----------
	model_name:
	X_train:
	y_train:
	X_test:
	y_test:
	param_grid:
	result_num:
	iter_num:
	n_proc：进程数
	executor：进程执行器

	Examples
	--------
	>>> import numpy as np
	>>> from sklearn.ensemble import RandomForestClassifier
	>>> from sklearn.model_selection import train_test_split
	>>> from sklearntools import search_model_params
	>>> X, y = np.arange(20).reshape((10, 2)), range(10)
	>>> X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
	>>> param_grid = {'n_estimators': np.arange(800, 820, 1), 'bootstrap': [False, True]}
	>>> search_model_params(RandomForestClassifier, X_train, y_train, X_test, y_test, param_grid, result_num=3)
	[{'bootstrap': False, 'n_estimators': 565}]
	"""
	sub_n_proc = None
	classifier = 'classifier' == model_name._estimator_type
	param_grid = ParameterGrid(param_grid)
	n_task = len(param_grid)
	logger.info(f'search_model_params 任务数：{n_task}')
	if executor is None:
		n_proc = get_processes(n_proc, n_task, 'search_model_params')
		if 1 == n_proc:
			sub_n_proc = 1
			results = [_search_params(model_name, classifier, X_train, y_train, X_test, y_test, params, verbose) for params in param_grid]
		else:
			with ProcessPoolExecutor(n_proc) as e:
				futures = [e.submit(_search_params, model_name, classifier, X_train, y_train, X_test, y_test, params, verbose) for
				           params in param_grid]
				results = [f.result() for f in as_completed(futures)]
	else:
		futures = [executor.submit(_search_params, model_name, classifier, X_train, y_train, X_test, y_test, params, verbose) for
		           params in param_grid]
		results = [f.result() for f in as_completed(futures)]
	results.sort(key=lambda x: x[1], reverse=True)
	params = []
	for param, score in results[:result_num]:
		params.append(param)
		if classifier:
			print(f'param: {param}\tscore: {score:.1%}')
		else:
			print(f'param: {param}\tscore: {score:.4f}')
		_evaluate_params(model_name, classifier, X_train, y_train, X_test, y_test, param, iter_num, sub_n_proc, executor)
	return params


def search_model_params_split(model_name, X, y, param_grid, test_size=0.2, result_num=5, iter_num=8, random_state=42,
                              n_proc: int = None, executor: ProcessPoolExecutor = None, verbose=False) -> list[dict]:
	"""Train and evaluate a model

	Parameters
	----------
	model_name:
	X:
	y:
	test_size:
	param_grid:
	result_num:
	iter_num:
	random_state:
	n_proc：进程数
	executor：进程执行器

	Examples
	--------
	>>> import numpy as np
	>>> from sklearn.ensemble import RandomForestClassifier
	>>> from sklearntools import search_model_params_split
	>>> X, y = np.arange(20).reshape((10, 2)), range(10)
	>>> param_grid = {'n_estimators': np.arange(800, 820, 1), 'bootstrap': [False, True]}
	>>> search_model_params_split(RandomForestClassifier, X, y, param_grid, test_size=0.2, result_num=3)
	[{'bootstrap': False, 'n_estimators': 565}]
	"""
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
	return search_model_params(model_name, X_train, y_train, X_test, y_test, param_grid, result_num, iter_num, n_proc, executor, verbose)


def search_test_size(model, X, y, test_sizes=np.arange(0.15, 0.36, 0.01), random_state=42, evaluate_fn=None,
                     n_proc: int = None, topK=5, executor: ProcessPoolExecutor = None, verbose=False) -> float:
	"""
	Examples
	--------
	>>> from sklearntools import search_test_size
	>>> search_test_size(model, X, y, random_state=42, evaluate_fn=accuracy_score)
	0.2
	"""
	classifier = 'classifier' == model._estimator_type
	n_task = len(test_sizes)
	logger.info(f'search_test_size 任务数：{n_task}')
	if executor is None:
		n_proc = get_processes(n_proc, n_task, 'search_test_size')
		if 1 == n_proc:
			results = [_search_test_size(model, X, y, test_size, random_state, evaluate_fn, verbose) for test_size in test_sizes]
		else:
			with ProcessPoolExecutor(n_proc) as e:
				futures = [e.submit(_search_test_size, model, X, y, test_size, random_state, evaluate_fn, verbose) for
				           test_size in test_sizes]
				results = [f.result() for f in as_completed(futures)]
	else:
		futures = [executor.submit(_search_test_size, model, X, y, test_size, random_state, evaluate_fn, verbose) for
		           test_size in test_sizes]
		results = [f.result() for f in as_completed(futures)]
	results.sort(key=lambda x: x[1], reverse=True)
	if classifier:
		for test_size, score in results[:topK]:
			print(f'test_size: {test_size:.0%} \t score: {score:.2%}')
	else:
		for test_size, score in results[:topK]:
			print(f'test_size: {test_size:.0%} \t score: {score:4f}')
	return results[0][0]


def search_random_state(model, X, y, random_states=np.arange(0, 20, 1), test_size=0.2, evaluate_fn=None,
                        n_proc: int = None, topK=5, executor: ProcessPoolExecutor = None, verbose=False) -> int:
	"""
	Examples
	--------
	>>> from sklearntools import search_random_state
	>>> search_random_state(model, X, y, test_size=0.2, evaluate_fn=accuracy_score)
	42
	"""
	classifier = 'classifier' == model._estimator_type
	n_task = len(random_states)
	logger.info(f'search_random_state 任务数：{n_task}')
	if executor is None:
		n_proc = get_processes(n_proc, n_task, 'search_random_state')
		if 1 == n_proc:
			results = [_search_random_state(model, X, y, test_size, random_state, evaluate_fn, verbose) for random_state in random_states]
		else:
			with ProcessPoolExecutor(n_proc) as e:
				futures = [e.submit(_search_random_state, model, X, y, test_size, random_state, evaluate_fn, verbose) for
				           random_state in random_states]
				results = [f.result() for f in as_completed(futures)]
	else:
		futures = [executor.submit(_search_random_state, model, X, y, test_size, random_state, evaluate_fn, verbose) for
		           random_state in random_states]
		results = [f.result() for f in as_completed(futures)]
	results.sort(key=lambda x: x[1], reverse=True)
	if classifier:
		for random_state, score in results[:topK]:
			print(f'random_state: {random_state} \t score: {score:.2%}')
	else:
		for random_state, score in results[:topK]:
			print(f'random_state: {random_state} \t score: {score:4f}')
	return results[0][0]


def _search_test_size(model, X, y, test_size, random_state, evaluate_fn, verbose=False):
	if verbose:
		pid = os.getpid()
		logger.info(f"进程：{pid} 开始 search_test_size test_size: {test_size:.2f}")
		start_time = time.perf_counter()
	result = train_evaluate_split(model, X, y, test_size, None, False, False, random_state, evaluate_fn)
	if verbose:
		logger.info(f"进程：{pid} 结束 search_test_size 耗时: {(time.perf_counter()-start_time):.2f} seconds.")
	return test_size, result


def _search_random_state(model, X, y, test_size, random_state, evaluate_fn, verbose=False):
	if verbose:
		pid = os.getpid()
		logger.info(f"进程：{pid} 开始 search_random_state random_state: {random_state}")
		start_time = time.perf_counter()
	result = train_evaluate_split(model, X, y, test_size, None, False, False, random_state, evaluate_fn)
	if verbose:
		logger.info(f"进程：{pid} 结束 search_random_state 耗时: {(time.perf_counter()-start_time):.2f} seconds.")
	return random_state, result


def _search_params(model_name, classifier, X_train, y_train, X_test, y_test, params, verbose=False):
	if verbose:
		pid = os.getpid()
		logger.info(f"进程：{pid} 开始 search_params params: {params}")
		start_time = time.perf_counter()
	model = model_name(**params)
	model.fit(X_train, y_train)
	score = model.score(X_test, y_test)
	if not classifier:
		score = round(score, 4)
	if verbose:
		logger.info(f"进程：{pid} 结束 search_params 耗时: {(time.perf_counter()-start_time):.2f} seconds.")
	return params, score


def _evaluate_params(model_name, classifier, X_train, y_train, X_test, y_test, params, iter_num, n_proc,
                     executor: ProcessPoolExecutor = None, verbose=False):
	if executor is None:
		n_proc = get_processes(n_proc, iter_num, 'evaluate_params')
		if 1 == n_proc:
			results = [_search_params(model_name, classifier, X_train, y_train, X_test, y_test, params, verbose) for _ in range(iter_num)]
		else:
			with ProcessPoolExecutor(n_proc) as e:
				futures = [e.submit(
					_search_params, model_name, classifier, X_train, y_train, X_test, y_test, params, verbose) for _ in range(iter_num)
				]
				results = [f.result() for f in as_completed(futures)]
	else:
		futures = [executor.submit(
			_search_params, model_name, classifier, X_train, y_train, X_test, y_test, params, verbose) for _ in range(iter_num)
		]
		results = [f.result() for f in as_completed(futures)]
		
	results = [result[1] for result in results]
	mean_score = sum(results) / len(results)
	
	counter = Counter(results)
	results = sorted(counter.items(), key=lambda x: x[0], reverse=True)
	if classifier:
		for score, count in results:
			print(f'\tscore: {score:.1%}\tcount: {count}')
		print(f'平均准确率: {mean_score:.1%}')
	else:
		for score, count in results:
			print(f'\tscore: {score:.4f}\tcount: {count}')
		print(f'平均分数: {mean_score:.4f}')


def multi_round_evaluate(X: np.ndarray, y: np.ndarray, *models, executor: ProcessPoolExecutor = None, verbose=False, **kwargs):
	""" 对比多个模型的稳定评分

	Parameters
	----------
	X:
	y:

	Examples
	--------
	>>> from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
	>>> from sklearntools import multi_round_evaluate
	>>> multi_round_evaluate(df.values, y, RandomForestClassifier(), GradientBoostingClassifier(), num_rounds=10, test_size=0.2)
	"""
	assert len(models) >= 1, 'models must be'
	num_rounds = kwargs.pop('num_rounds') if 'num_rounds' in kwargs else 100
	test_size = kwargs.pop('test_size') if 'test_size' in kwargs else 0.2
	if executor is None:
		n_proc = kwargs.pop('n_proc') if 'n_proc' in kwargs else None
		n_proc = get_processes(n_proc, num_rounds, 'multi_round_evaluate')
		with ProcessPoolExecutor(n_proc) as e:
			futures = [e.submit(one_round_evaluate, X, y, test_size, *models) for _ in range(num_rounds)]
			results = [f.result() for f in as_completed(futures)]
	else:
		futures = [executor.submit(one_round_evaluate, X, y, test_size, *models, verbose=verbose) for _ in range(num_rounds)]
		results = [f.result() for f in as_completed(futures)]
	results = np.array(results)
	return results.mean(axis=0)


def one_round_evaluate(X: np.ndarray, y: np.ndarray, test_size: float, *models, verbose=False) -> float:
	if verbose:
		pid = os.getpid()
		logger.info(f"进程：{pid} 开始 one_round_evaluate")
	scores = []
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=11)
	for i, model in enumerate(models):
		model.fit(X_train, y_train)
		scores.append(model.score(X_test, y_test))
	if verbose:
		logger.info(f"进程：{pid} 开始 one_round_evaluate")
	return scores


def get_processes(n_proc, n_task, fn_name: str):
	cpu_count = os.cpu_count()
	n_proc = min(n_proc, cpu_count, n_task) if n_proc else min(cpu_count, n_task)
	logger.info(f'{fn_name} 进程数: {n_proc}')
	return n_proc
