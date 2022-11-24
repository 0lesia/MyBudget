import sqlite3


def create_db():
    con = sqlite3.connect('myBudget.sqlite')
    with con:
        cur = con.cursor()
        cur.executescript("""
                        create table if not exists fin_sources(
                                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, 
                                name text UNIQUE
                        );
                        create table if not exists categories(
                                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, 
                                name text UNIQUE
                        );
                        create table if not exists transactions(
                                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, 
                                date date NOT NULL, 
                                category int NOT NULL,
                                source int NOT NULL,
                                amount float,
                                description text
                        );
                        """)
        con.commit()
        cur.close()


def getSourceId(cur, data):
    cur.execute('select id from fin_sources where name = ?', (data,))
    val = cur.fetchone()
    if val is None:
        cur.execute('insert into fin_sources (name) values (?)', (data,))
        val = cur.lastrowid
    else:
        val = val[0]
    return val


def getCategoryId(cur, data):
    cur.execute('select id from categories where name = ?', (data,))
    val = cur.fetchone()
    if val is None:
        cur.execute('insert into categories (name) values (?)', (data,))
        val = cur.lastrowid
    else:
        val = val[0]
    return val


def addTransaction(dateT, sourceT, categoryT, amountT, commentT):
    con = sqlite3.connect('myBudget.sqlite')
    with con:
        cur = con.cursor()
        idSource = getSourceId(cur, sourceT)
        idCategory = getCategoryId(cur, categoryT)
        con.commit()

        cur.execute('''insert or replace into transactions (date, category, source, amount, description)
                        values (?,?,?,?,?)''', (dateT, idCategory, idSource, amountT, commentT))
        cur.close()

def getTransactions(date_from, date_to, aggregate = False):
    con = sqlite3.connect('myBudget.sqlite')
    with con:
        cur = con.cursor()
        textQuery = '''select
                            strftime('%m',transactions.date),
                            categories.name,
                            fs.name,
                            sum(transactions.amount)
                        from transactions
                            left join categories on categories.id = transactions.category
                            left join fin_sources fs on fs.id = transactions.source
                        where date >= ? and date <= ?
                        group by
                            strftime('%m',transactions.date),
                            categories.name,
                            fs.name
                        order by
                            strftime('%m',transactions.date),
                            fs.name,
                            categories.name'''
        query_result = cur.execute(textQuery, (date_from,date_to))
        for row in query_result:
            print(row)