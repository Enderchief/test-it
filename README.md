# TestIt
### *The Simple Testing Framework*

___

## How to use
Create a `tests` folder in your project root.
### Organization
- Each Python file in `tests`
- Each function that start with `test_` and has the `@test` decorator
- Each individul test in the function

## A basic test
Project code in `main.py`
```python
def fib(n):
	a, b = 0, 1
	if n <= 2:
		return n
	for _ in range(2, n+1):
		a, b = b, a+b
	return b
```

In `tests/foo.py`
```python
from testit import test, Test

@test('test that the output of fibonacci sequence is accurate')
def test_accurate(t: 'Test'):
	t.expect(fib, 1).equal(1).message('fib of 1 should be 1')
	t.expect(fib, 5).equal(5).message('fib of 5 should be 5')
	t.expect(fib, 10).equal(55).message('fib of 10 should be 55')


@test('test that the wrong numbers dont work')
def test_wrong(t: 'Test'):
	t.expect(fib, 2).not_equal(3).message('fib of 2 should not be 2')
	t.expect(fib, 10).not_equal(55).message('fib of 10 should not be 55')
	
```
Output after running `python -m testit`
<pre>
<span style="background:#0DBC79;color:white;"> PASS </span> <span style="color:yellow;font-weight:600">test_accurate - test that the output of fibonacci sequence is accurate</span>
<span style="color:#0DBC79;">✓</span> fib of 1 should be 1
<span style="color:#0DBC79;">✓</span> fib of 5 should be 5
<span style="color:#0DBC79;">✓</span> fib of 10 should be 55


<span style="background:#CD3131;color:white;"> FAIL </span> <span style="color:yellow;font-weight:600">test_wrong - test that the wrong numbers dont work</span>
<span style="color:#0DBC79;">✓</span> fib of 2 should not be 2
<span style="color:#CD3131">✗</span> fib of 10 should not be 55
   <span style="color:#CD3131">- Expected:</span>		fib(<span style="color:yellow">10</span>) != <span style="color:yellow">55</span>
   <span style="color:#CD3131">+ Recieved value:</span>	<span style="color:yellow">55</span>

</pre>

---