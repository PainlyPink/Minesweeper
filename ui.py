import threading
import time


def lazy_range(a, b=None, step=1):
  if b:
    while a < b:
      yield a
      a += step
  else:
    i = 0
    while i < a:
      yield i
      i += step


def range_test(builtin):
  start = time.perf_counter()
  n = 10000000
  if builtin:
    for _ in range(n):
      pass
  else:
    for _ in lazy_range(n):
      pass
  end = time.perf_counter()
  print(f"{'Built-in range ' if builtin else 'Lazy range '} took {end-start:.4f} seconds")


def main():
  threads = []
  for builtin in [True, False]:
    thread = threading.Thread(target=range_test, args=(builtin,))
    thread.start()
    threads.append(thread)
  for thread in threads:
    thread.join()


if __name__ == "__main__":
  main()
