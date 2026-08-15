# Pandas has 2 basic data structures: 
 - Series: 1-D labeled array holding and data type
 - DataFrame: 2-D structure that holds data like a chart of rows and columns

# Creating objects:
## You can create a series by passing in a list of values. Pandas will either give it a default index, or you can make your own
In [3]: s = pd.Series([1, 3, 5, np.nan, 6, 8])

In [4]: s
Out[4]: 
0    1.0
1    3.0
2    5.0
3    NaN
4    6.0
5    8.0
dtype: float64


## You can create a dataframe by passing in an array with indexes
In [9]: df2 = pd.DataFrame(
   ...:     {
   ...:         "A": 1.0,
   ...:         "B": pd.Timestamp("20130102"),
   ...:         "C": pd.Series(1, index=list(range(4)), dtype="float32"),
   ...:         "D": np.array([3] * 4, dtype="int32"),
   ...:         "E": pd.Categorical(["test", "train", "test", "train"]),
   ...:         "F": "foo",
   ...:     }
   ...: )
   ...: 

In [10]: df2
Out[10]: 
     A          B    C  D      E    F
0  1.0 2013-01-02  1.0  3   test  foo
1  1.0 2013-01-02  1.0  3  train  foo
2  1.0 2013-01-02  1.0  3   test  foo
3  1.0 2013-01-02  1.0  3  train  foo 

**Notice, for columns like F, 'foo' was passed in once, but since a column like E had 4 inputs, it repeats**

## You can also see the dtypes of each columns
In [11]: df2.dtypes
Out[11]: 
A           float64
B    datetime64[us]
C           float32
D             int32
E          category
F               str
dtype: object



# Viewing data
**df** --> represents dummy name for a dataframe in upcoming notes:
**df.head()** - view top few rows --> defaults to 5, or specify number in the parameter
**df.tail()** - view last few rows, same rules as above

**df.index()** - displays the row labels
**df.columns()** - displays column labels

**df.to_numpy()** - converts df to a numpy matrix with no index/column labels
   --> Numpy arrays only have 1 dtype in the entire array
   --> if df is mixed types, it will store it as an object dtype (sim to a pointer)

**df.describe()** - quick stats about data (count, mean, std, min, quartiles, max of the columns)

**df.T** - transpose of the array

**df.sort_index**(axis = __(google parameters for what this means)__, ascending = ____(T/F)_)
 - sorts by an axis (I think that means the indexes or columns)
**df.sort_values**(by=____column label___) - self explanitory


# Selection
**Pandas has optimized methods to access data that are stronger and more efficient than typical selecting and setting expressions**
For the following selection methods, assume the following df
      'A'      'B'      'C'
2-9   1        2        3
4-16  2        3        4
5-23  3        4        5
8-9   4        5        6  
9-7   5        6        7

## Getitem ([])
Typical indexing
df['A'] --> or df.A
**Output**
2-9      1
4-16     2
5-23     3
8-9      4
9-7      5

slice (100:110) --> checks rows
boolean mask (pbp_pd['down'] == 4) --> checks rows
string, individual data point, list of strings or other data