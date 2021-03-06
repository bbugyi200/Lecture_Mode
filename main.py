import keyhooks
import dmenu
import sqlite3
import public as pub
import latex

DB_Path = 'topics.db'
DB_Connection = sqlite3.connect(DB_Path)
DB = DB_Connection.cursor()


def getAllTopics() -> "List of Strings":
    try:
        DB.execute('SELECT * FROM topics')
        return [entry[0] for entry in DB.fetchall()]
    except sqlite3.OperationalError:
        DB.execute('CREATE TABLE topics (topic text)')
        return []


def main():
    Topics_List = getAllTopics()
    pub.topic = dmenu.show(Topics_List)

    if pub.topic not in Topics_List:
        prompt = 'Would you like to save this topic for future use (y/n)?: '
        choice = dmenu.show([], prompt=prompt)
        if choice.lower() == 'y':
            DB.execute('INSERT INTO topics VALUES (?)', (pub.topic,))
            DB_Connection.commit()

    pub.LatexDoc = latex.LatexDoc()
    keyhooks.start()


if __name__ == '__main__':
    main()
