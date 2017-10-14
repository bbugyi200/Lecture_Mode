import latex
import keyhooks
import dmenu
import sqlite3

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
    topic = dmenu.show(Topics_List)

    if topic not in Topics_List:
        prompt = 'Would you like to save this topic for future use (y/n)?: '
        choice = dmenu.show([], prompt=prompt)
        if choice.lower() == 'y':
            DB.execute('INSERT INTO topics VALUES (?)', (topic,))
            DB_Connection.commit()

    latex.build(topic)
    keyhooks.start()


if __name__ == '__main__':
    main()
