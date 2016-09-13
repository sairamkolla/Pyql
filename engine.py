from parser import MyParse
import os
import copy

schema = []
tables = []
operations = ["sum", "average", "min", "max", "distinct"]


def init_engine():
    ot = open("content/welcome.txt", "r")
    print ot.read(),
    l = open("metadata.txt", "r")
    l = l.read()
    l = l.split("<begin_table>")
    for i in l:
        if len(i):
            schema.append(i.split()[:-1])
            tables.append(i.split()[0])
    print tables
    print schema
    return


def find_table(table_name):
    global tables
    for x in tables:
        if x == table_name:
            return tables.index(x)
    return -1


def find_column(tno, column_name):
    global schema
    table = schema[tno][1:]
    for col in table:
        if col == column_name:
            return table.index(col)
    return -1


def sum_col(colno, tno):
    global tables
    sum_value = 0
    x = open(tables[tno] + '.csv', 'r')
    x = x.read()
    x = x.split('\n')
    for i in x:
        sum_value += int(i.strip().split(',')[colno])
    return sum_value


def average_col(colno, tno):
    global tables
    sum_value = 0
    x = open(tables[tno] + '.csv', 'r')
    x = x.read()
    x = x.split('\n')
    for i in x:
        sum_value += int(i.strip().split(',')[colno])
    return sum_value / len(x)


def min_col(colno, tno):
    global tables
    min_value = 10000000000
    x = open(tables[tno] + '.csv', 'r')
    x = x.read()
    x = x.split('\n')
    for i in x:
        num = int(i.strip().split(',')[colno])
        if num < min_value:
            min_value = num
    return min_value


def max_col(colno, tno):
    global tables
    max_value = -10000000000
    x = open(tables[tno] + '.csv', 'r')
    x = x.read()
    x = x.split('\n')
    for i in x:
        num = int(i.strip().split(',')[colno])
        if num > max_value:
            max_value = num
    return max_value


def col_single_op(cno, tno, op):
    global operations
    global schema
    options = {0: sum_col,
               1: average_col,
               2: min_col,
               3: max_col}
    value = options[op](cno, tno)
    print operations[op] + '(' + schema[tno][cno + 1] + ')'
    print value
    return


def kill_engine():
    ct = open("content/bye.txt", "r")
    print ct.read(),
    return

def rename_where(where_condition,a):
    if len(where_condition) > 1:
        cns = where_condition[1:]

        #print cns
        for i in range(0,len(cns)+1,2):
            for j in [0,2]:
                temp = cns[i][j]
                if len(temp.split('.')) == 2:
                    pass
                else:
                    col = cns[i][j]
                    for table in a.tables:
                        if not find_column(find_table(table), col) == -1:
                            cns[i][j] = table + '.' + col
                            break
        #print cns
        return cns
    return [-1]

def calculator(a,b,symbol):
    a = int(a)
    b = int(b)
    if symbol == '<':
        return a < b
    elif symbol == '>':
        return a > b
    elif symbol == '=':
        return a == b

def evaluate(row,ref_list,where_cn):
    if len(where_cn) > 1:
        c1 = where_cn[0]
        c2 = where_cn[2]
        op = where_cn[1]
        if op == 'or':
            return calculator(row[ref_list.index(c1[0])],row[ref_list.index(c1[2])],c1[1]) or calculator(row[ref_list.index(c2[0])],row[ref_list.index(c2[2])],c2[1])
        elif op == 'and':
            return calculator(row[ref_list.index(c1[0])], row[ref_list.index(c1[2])], c1[1]) and calculator(row[ref_list.index(c2[0])], row[ref_list.index(c2[2])], c2[1])
    else:
        c1 = where_cn[0]
        return calculator(row[ref_list.index(c1[0])],row[ref_list.index(c1[2])],c1[1])
    return 1

def print_data2(query,m,cols_list,ref_list,where_cn):
    #print "in print data function"
    if len(query.where[0]) < 1:
        #print "Where condition is not there"
        for row in cols_list[:-1]:
            print row + ',',
        print cols_list[-1]
        for row in m:
            for col in cols_list[:-1]:
                print row[ref_list.index(col)] + ',',
            print row[ref_list.index(cols_list[-1])]
    else:

        print "where condition is there"
        for row in cols_list[:-1]:
            print row + ',',
        print cols_list[-1]
        for row in m:
            #print evaluate(row, ref_list, where_cn)
            if evaluate(row, ref_list, where_cn):
                for col in cols_list[:-1]:
                        print row[ref_list.index(col)] + ',',
                print row[ref_list.index(cols_list[-1])]

            #print where_cn

    return
def distinct_data(cols,tno):
    return


def check_tables(tlist):
    global tables
    for table in tlist:
        if table not in tables:
            print "Query cannot be processed. One or more tables is missing."
            return -1
    if len(set(tlist)) < len(tlist):
        print "Query cannot be processed. One or more tables are repeating."
        return -1
    return 1


def check_columns(a):
    if len(a.columns) == 1 and a.columns[0] == "*" and len(a.where[0]) < 1:
        return 1
    if not a.columns[0] == "*":
        for col in a.columns:
            if len(col.split('.')) ==2:
                #print col.split('.')
                col_temp = col.split('.')[1]
                table = col.split('.')[0]
                if table in list(a.tables):
                    if not find_column(find_table(table), col_temp) == -1:
                        pass
                    else:
                        print "Query cannot be processed. One or more columns is not found."
                else:
                    print "Query cannot be processed. One or more tables is not found."
                    return -1
                continue
            found = 0
            for table in a.tables:
                if  not find_column(find_table(table),col) == -1:
                    found = 1
                    break
            if found == 0:
                #print col
                print "Query cannot be processed. One or more columns is not found."
                return -1
    #print "for processing where condition"
    if len(a.where[0]) > 1:
        #print "checking"
        cns = copy.deepcopy(a.where[0][1:])
        for i in range(0,len(cns)+1,2):
            #print "checking ",i," condition"
            for j in [0,2]:
                temp = cns[i][j]
                if len(temp.split('.')) == 2:
                    col = temp.split('.')[1]
                    table = temp.split('.')[0]
                    #print table
                    #print a.tables[0]
                    if table in list(a.tables):
                            if  not find_column(find_table(table), col) == -1:
                                pass
                            else:
                                print "Query cannot be processed. One or more columns is not found."
                    else:
                        print "Query cannot be processed. One or more tables is not found."
                        return -1
                else:
                    col = cns[i][j]
                    found = 0
                    for table in a.tables:
                        if not find_column(find_table(table), col) == -1:
                            found = 1
                            break
                    if found == 0:
                        #print col
                        print "Query cannot be processed. One or more columns is not found."
                        return -1

    return 1

def get_data(a):
    global schema
    global tables
    m = []
    cols_list = []
    temp = open(a.tables[0] + '.csv','r')
    temp = temp.read()
    temp = temp.split('\n')
    for x in temp:
        m.append(x.strip().split(','))
    cols_list += [a.tables[0] + '.' + x for x in schema[find_table(a.tables[0])][1:]]
    #print m
    for table in a.tables[1:]:
        prev_data = copy.deepcopy(m)
        m = []
        temp = open(table + '.csv', 'r')
        temp = temp.read()
        temp = temp.split('\n')
        #print temp
        for record in prev_data:
            for x in temp:
                m.append(record + x.strip().split(','))
        cols_list +=  [table + '.' + x for x in  schema[find_table(table)][1:]]
    #print m
    #print cols_list
    #print len(m)
    return m,cols_list
def rename_columns(a):
    global schema
    global tables
    cols = []
    for col in a.columns:
        if len(col.split('.')) == 2:
            cols.append(col)
        else:
            for table in a.tables:
                if not find_column(find_table(table),col) == -1:
                    cols.append(table + '.' + col)
                    break
    return cols

def process(a):
    if not check_tables(a.tables) == -1 and not check_columns(a) == -1:
        m,ref_list = get_data(a)
        if len(a.columns) == 1 and a.columns[0] == "*":
            cols_list = ref_list
        else:
            cols_list = rename_columns(a)
        temp  = copy.deepcopy(a.where)[0]

        where_cn = rename_where(temp,a)
        print a
        #print m
        print where_cn
        print ref_list
        print cols_list
        #print len(m)

        print_data2(a,m,cols_list,ref_list,where_cn)
    return
def run_engine():
    prompt = ">>>  "
    while 1:
        x = raw_input(prompt)
        if x.strip() in ["exit", "quit"] and len(x):
            break
        if x.strip() in ["clear", "cc"]:
            os.system("clear")
        elif len(x):
            a = MyParse(x)
            if not a == 0:
                #print a
                process(a)
        else:
            pass


if __name__ == "__main__":
    init_engine()
    run_engine()
    kill_engine()
