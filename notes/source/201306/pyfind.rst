========================
Python Find 源码
========================

首先找到string.find定义的地方， 在Objects/stringobject.c::
      
  static PyObject *  
  string_find(PyStringObject *self, PyObject *args)  
  {  
      Py_ssize_t result = string_find_internal(self, args, +1);  
      if (result == -2)  
          return NULL;  
      return PyInt_FromSsize_t(result);  
  }  
    
  Py_LOCAL_INLINE(Py_ssize_t)  
  string_find_internal(PyStringObject *self, PyObject *args, int dir)
  {  
      PyObject *subobj;  
      const char *sub;  
      Py_ssize_t sub_len;  
      Py_ssize_t start=0, end=PY_SSIZE_T_MAX;  
      PyObject *obj_start=Py_None, *obj_end=Py_None;  
    
      ....  
    
      if (dir > 0) 
          /* 正向查找 */
          return stringlib_find_slice(  
              PyString_AS_STRING(self), PyString_GET_SIZE(self),  
              sub, sub_len, start, end);  
      else  
          /* 逆向查找 */
          return stringlib_rfind_slice(  
              PyString_AS_STRING(self), PyString_GET_SIZE(self),  
              sub, sub_len, start, end);  
  }  
    

stringlib_find_slice 定义在 Objects/stringlib/find.h::
    
  Py_LOCAL_INLINE(Py_ssize_t)  
  stringlib_find_slice(const STRINGLIB_CHAR* str, Py_ssize_t str_len,  
                       const STRINGLIB_CHAR* sub, Py_ssize_t sub_len,  
                       Py_ssize_t start, Py_ssize_t end)  
  {  
      ADJUST_INDICES(start, end, str_len);  
      return stringlib_find(str + start, end - start, sub, sub_len, start);  
  }  
    
  Py_LOCAL_INLINE(Py_ssize_t)  
  stringlib_find(const STRINGLIB_CHAR* str, Py_ssize_t str_len,  
                 const STRINGLIB_CHAR* sub, Py_ssize_t sub_len,  
                 Py_ssize_t offset)  
  {  
      Py_ssize_t pos;  
    
      if (str_len < 0)  
          return -1;  
      if (sub_len == 0)  
          return offset;  
    
      pos = fastsearch(str, str_len, sub, sub_len, -1, FAST_SEARCH);  
    
      if (pos >= 0)  
          pos += offset;  
    
      return pos;  
  }  
   
fastsearch 定义在 Objects/stringlib/fastsearch.h, 先是些宏定义::
    
  #if LONG_BIT >= 128  
  #define STRINGLIB_BLOOM_WIDTH 128  
  #elif LONG_BIT >= 64  
  #define STRINGLIB_BLOOM_WIDTH 64  
  #elif LONG_BIT >= 32  
  #define STRINGLIB_BLOOM_WIDTH 32  
  #else  
  #error "LONG_BIT is smaller than 32"  
  #endif  
    
  #define STRINGLIB_BLOOM_ADD(mask, ch) \  
      ((mask |= (1UL << ((ch) & (STRINGLIB_BLOOM_WIDTH -1)))))  
  #define STRINGLIB_BLOOM(mask, ch)     \  
      ((mask &  (1UL << ((ch) & (STRINGLIB_BLOOM_WIDTH -1)))))  

STRINGLIB_BLOOM 和 STRINGLIB_BLOOM_ADD 这里是构建了一个字符的bloom-filter, STRINGLIB_BLOOM_ADD简单来说就是 mask =| 1 << int(ch), STRINGLIB_BLOOM 是 mask & ( 1 << int(ch) )

具体的实现::
    
  Py_LOCAL_INLINE(Py_ssize_t)  
  fastsearch(const STRINGLIB_CHAR* s, Py_ssize_t n,  
             const STRINGLIB_CHAR* p, Py_ssize_t m,  
             Py_ssize_t maxcount, int mode)  
  {  
      unsigned long mask;  
      Py_ssize_t skip, count = 0;  
      Py_ssize_t i, j, mlast, w;  
    
      w = n - m; //n是查找串长度，m是子串长度 
    
      if (w < 0 || (mode == FAST_COUNT && maxcount == 0))  
          return -1;  
    
      /* look for special cases */  
      if (m <= 1) {  
          if (m <= 0)  
              return -1;  
          /* use special case for 1-character strings */  
          ...  
          if (mode == FAST_SEARCH) {  //子串长度为1时直接循环比较
              for (i = 0; i < n; i++)  
                  if (s[i] == p[0])  
                      return i;  
          } else {    /* FAST_RSEARCH */  
              for (i = n - 1; i > -1; i--)  
                  if (s[i] == p[0])  
                      return i;  
          }  
          return -1;  
      }  
    
      mlast = m - 1;  
      skip = mlast - 1;  
      mask = 0;  
    
      if (mode != FAST_RSEARCH) {  
    
          /* create compressed boyer-moore delta 1 table */  
    
          /* process pattern[:-1] */  
          for (i = 0; i < mlast; i++) {  
              STRINGLIB_BLOOM_ADD(mask, p[i]);  
              if (p[i] == p[mlast])  
                  skip = mlast - i - 1; //计算skip,只取最小值  
          }  
          /* process pattern[-1] outside the loop */  
          STRINGLIB_BLOOM_ADD(mask, p[mlast]);  
    
          for (i = 0; i <= w; i++) {  
              /* note: using mlast in the skip path slows things down on x86 */  
              if (s[i+m-1] == p[m-1]) {  
                  /* candidate match */  
                  for (j = 0; j < mlast; j++) //最后一个字符匹配后再从第一个字符往后匹配 
                      if (s[i+j] != p[j])  
                          break;  
                  if (j == mlast) {  // 完全匹配成功
                      /* got a match! */  
                      if (mode != FAST_COUNT)  
                          return i;  
                      count++; // 在要求查找所有匹配的情况下，继续匹配
                      if (count == maxcount)  
                          return maxcount;  
                      i = i + mlast;  
                      continue;  
                  }  
                  /* miss: check if next character is part of pattern */  
                  if (!STRINGLIB_BLOOM(mask, s[i+m])) //不匹配，且下一个字符不是子串中字符 
                      i = i + m; //直接跳过整个子串长度 
                  else  
                      i = i + skip; //下一字符是子串字符，跳过skip个字符 
              } else {  
                  /* skip: check if next character is part of pattern */  
                  //尾字符不匹配时，如后面一个字符也不可能匹配，直接跳过子串长度， 否则＋1
                  if (!STRINGLIB_BLOOM(mask, s[i+m]))  
                      i = i + m;  
              }  
          }  
      } else {    /* FAST_RSEARCH */  
    
          ...  
      }  
    
      if (mode != FAST_COUNT)  
          return -1;  
      return count;  
  } 

从源码看来，string.find使用的是简化BM算法，虽然某些场景效率不是最高，但胜在实现简单，性能也不错。
