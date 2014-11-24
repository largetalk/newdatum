=========================
some trick
========================

Size balance tree
=====================

size balance tree is 一种通过大小（size）域来保持平衡的二叉搜索树， 它总满足：
  1. s[right(t)] >= s[left[left(t)]], s[right[left(t)]]
  2. s[left(t)] >= s[right[right(t)]], s[left[right(t)]]
  即，每棵子树的大小不小于其兄弟的子树大小

left-rotate(t):
  k = right[t]
  right[t] = left[k]
  left[k] = t
  s[k] = s[t]
  s[t] = s[left[t]] + s[right[t]] + 1
  t = k

right-rotate(t):
  k = left[t]
  left[t] = right[k]
  right[k] = t
  s[k] = s[t]
  s[t] = s[left[t]] + s[right[t]] + 1
  t = k

quick sort
==============

void qsort(int a[], int low, int high) {
  if (low >= high) {
    return;
  }
  int first = low;
  int last = high;
  int key = a[first];
  while (first < last) {
    while (first < last && a[last] >= key) {
      last--;
    }
    a[first] = a[last];
    while (first < last && a[first] <= key) {
      first++;
    }
    a[last] = a[first];
  }
  a[first] = key;
  qsort(a, low, first - 1);
  qsort(a, first + 1, high);
}
