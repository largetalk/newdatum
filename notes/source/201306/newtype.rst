===========================
Python New Type
===========================


如上节所说，python允许编写一个扩展模块来定义新的类型，新类型能用python代码操纵，向python核心中的string和list一样。

这并不困难，所有扩展类型代码都遵循一种模式，但有些细节需要明白在你开始之前。

2.1 基础
==========================

python运行时环境把所有python对象都看做类型PyObject*的对象。Pyobject不是一个有魔术的对象-它只是包含引用计数和指向对象指针的“类型对象”。这就是关键所在，类型对象决定哪个（C）函数何时被调用，比如，属性查找时或与其他对象相乘时。这个C函数被叫做类型方法。

所以，如果你想定义一种新的对象类型， 你需要创建一个新的类型对象.

这些事情能通过例子来解释，这里是一个最低限度，但是完整的创建一个新类型的模块

    #include <Python.h>
    
    typedef struct {

        PyObject_HEAD

        /* Type-specific fields go here. */

    } noddy_NoddyObject;
    

    static PyTypeObject noddy_NoddyType = {

        PyObject_HEAD_INIT(NULL)

        0,                         /*ob_size*/

        "noddy.Noddy",             /*tp_name*/

        sizeof(noddy_NoddyObject), /*tp_basicsize*/

        0,                         /*tp_itemsize*/

        0,                         /*tp_dealloc*/

        0,                         /*tp_print*/

        0,                         /*tp_getattr*/

        0,                         /*tp_setattr*/

        0,                         /*tp_compare*/

        0,                         /*tp_repr*/

        0,                         /*tp_as_number*/

        0,                         /*tp_as_sequence*/

        0,                         /*tp_as_mapping*/

        0,                         /*tp_hash */

        0,                         /*tp_call*/

        0,                         /*tp_str*/

        0,                         /*tp_getattro*/

        0,                         /*tp_setattro*/

        0,                         /*tp_as_buffer*/

        Py_TPFLAGS_DEFAULT,        /*tp_flags*/

        "Noddy objects",           /* tp_doc */

    };

    
    static PyMethodDef noddy_methods[] = {

        {NULL}  /* Sentinel */

    };

    
    #ifndef PyMODINIT_FUNC	/* declarations for DLL import/export */

    #define PyMODINIT_FUNC void

    #endif

    PyMODINIT_FUNC

    initnoddy(void) 

    {

        PyObject* m;
    
        noddy_NoddyType.tp_new = PyType_GenericNew;

        if (PyType_Ready(&noddy_NoddyType) < 0)

            return;
    
        m = Py_InitModule3("noddy", noddy_methods,

                           "Example module that creates an extension type.");
    
        Py_INCREF(&noddy_NoddyType);

        PyModule_AddObject(m, "Noddy", (PyObject *)&noddy_NoddyType);

    }


一下子看起来有点多，但希望有些和上一章看起来有点相似。

第一部分新的是：

  typedef struct {

      PyObject_HEAD

  } noddy_NoddyObject;

这是一个Noddy 对象包含的-在这个例子中，比任一python对象包含的都少，仅仅只有一个引用计数和类型对象的指针。他们包含在PyObject_HEAD宏里。宏的作用是标准化布局并且可以在debug构建时启用debug字段。注意，PyObject_HEAD宏后面没有分号,分号包括在宏定义里了。小心别意外多添加了一个，很容易由于习惯这么做，你的编译器可能不会报错，但是别人的可能会（在windows平台，已知MSVC有此错误并且拒绝编译代码）

作为对比，让我们看看标准python整型的定义

  typedef struct {
  
      PyObject_HEAD

      long ob_ival;

  } PyIntObject;


继续，我们来到了关键地方-类型对象

    static PyTypeObject noddy_NoddyType = {
        PyObject_HEAD_INIT(NULL)
        0,                         /*ob_size*/
        "noddy.Noddy",             /*tp_name*/
        sizeof(noddy_NoddyObject), /*tp_basicsize*/
        0,                         /*tp_itemsize*/
        0,                         /*tp_dealloc*/
        0,                         /*tp_print*/
        0,                         /*tp_getattr*/
        0,                         /*tp_setattr*/
        0,                         /*tp_compare*/
        0,                         /*tp_repr*/
        0,                         /*tp_as_number*/
        0,                         /*tp_as_sequence*/
        0,                         /*tp_as_mapping*/
        0,                         /*tp_hash */
        0,                         /*tp_call*/
        0,                         /*tp_str*/
        0,                         /*tp_getattro*/
        0,                         /*tp_setattro*/
        0,                         /*tp_as_buffer*/
        Py_TPFLAGS_DEFAULT,        /*tp_flags*/
        "Noddy objects",           /* tp_doc */
    };

现在如果你去查看PyTypeObject在object.h中的定义，你会看到比上面定义多的多的字段。余下的字段C编译器会用0来填充，所以如果你不需要他们时一般不须去显示指定他们。

我们要挑最重要的部分进行下去是很重要的：

    PyObject_HEAD_INIT(NULL)

这行有点缺点，我们喜欢这样写：

    PyObject_HEAD_INIT(&PyType_Type)

正如类型对象的类型是"type"， 但是不是严格遵循C,有些编译器会报错。幸运的是，该成员会被PyType_Ready填充

    0,                          /﹡ ob_size﹡/

头部的ob_size没有被使用，它的存在是因为历史原因，为了保证与旧版本python编译的扩展模块兼容, 一般把该字段设为0

   "noddy.Noddy",              /* tp_name */

该类型的名称，它会显示在对象默认的文字表达和一些错误消息中， 如：

    >>> "" + noddy.new_noddy()

    Traceback (most recent call last):

      File "<stdin>", line 1, in ?

      TypeError: cannot add type "noddy.Noddy" to string

注意，名字是有点的名字，包括模块名和模块中类型的名字。这个例子中模块的名字是noddy,类型是Noddy, 所以我们设置类型名为noddy.Noddy

    sizeof(noddy_NoddyObject),  /* tp_basicsize */

这让python知道需要分配多少内存，当我们调用PyObject_New()

  注意：如果你想你的类型是可继承的，并且你的类型和它的基类有同样的tp_basicsize, 你可能在多继承时会遇到问题。 一个继承于你的类型的python子类会在他的__bases__中列出你的类型， 否则将不能正确调用你类型的__new__()方法。你可以通过确保你的类型的tp_basicsize值大于它的基类来避免该问题。大多数情况下，这都正确， 因为要么你的基类是object,或者添加数据成员到基类中，从而增加它的大小。

    0,                          /* tp_itemsize */

这会被可变长度对象如list和string用到，现在先忽略。

略过我们暂不提供的类型方法， 我们设置类flag为Py_TPFLAGS_DEFAULT.

    Py_TPFLAGS_DEFAULT,        /*tp_flags*/

所有类型在它们的flag里都应该包含这个常量。它启用了所有被当前版本python定义的成员。

我们为类型的tp_doc提供一个string

    "Noddy objects",           /* tp_doc */
