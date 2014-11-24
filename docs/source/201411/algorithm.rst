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

maintain:

当插入和删除一个节点之后，sbt的性质就有可能被改变，这时需要用maintain来修复

case 1：s[left[left[t]]] > s[right[t]]

  先right-rotate(t)
  这之后，有时，这棵树可能还不是SBT， 所以仍有必要调用maintain(t)
  节点L的右子树可能被连续调整，所以可能由于性质被破坏需要运行maintain(L)

case 2: s[right[left[t]]] >= s[right[t]]

  先left-rotate(L)
  然后执行right-rotate(t)
  maintain(L) 和 maintain(T)
  在第3步之后，子树都已经是SBT，但新根节点B可能还不是， 所以maintain(B)

case 3: s[right[right[t]]] > s[left[t]]

  与case 1对称

case 4: s[left[right[t]]] > s[left[t]]

  与case 2对称



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
