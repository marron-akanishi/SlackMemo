from slackbot.bot import respond_to
from slackbot.bot import listen_to
from slackbot.bot import default_reply
import libs.db_utils as db

@default_reply
def default_respond(message):
    message.reply("そのコマンドは理解できません")

# チャンネル
@listen_to(r'.+')
def listen_func(message):
    text = message.body['text']
    command = text[:6]
    body = text[6:]
    if command == "!save ":
        save_func(body, message)
    elif command == "!load ":
        load_func(body, message)
    elif command == "!dele ":
        delete_func(body, message)
    elif text == "!list":
        list_func(message)
    elif text == "!help":
        help_func(message)

# DM
@respond_to(r'.+')
def all_respond_func(message):
    text = message.body['text']
    command = text[:5]
    body = text[5:]
    if command == "save ":
        save_func(body, message)
    elif command == "load ":
        load_func(body, message)
    elif command == "dele ":
        delete_func(body, message)
    elif text == "list":
        list_func(message)
    elif text == "help":
        help_func(message)
    else:
        default_respond(message)

def save_func(text, message):
    title = text.split("\n")[0]
    detail = text.split("\n")[1]
    if title == "":
        message.reply("タイトルを指定してください")
        return
    titlelist = db.get_list(message.body['channel'])
    if title in titlelist:
        db.update_memo(message.body['channel'], title, detail)
        message.reply("メモを編集しました: {}".format(title))
    else:
        db.write_memo(message.body['channel'], title, detail)
        message.reply("メモをセーブしました: {}".format(title))

def load_func(text, message):
    memo = db.get_detail(message.body['channel'], text)
    if memo == None:
        message.reply("そのようなメモは存在しません")
    else:
        message.reply("{}\n{}".format(memo['title'], memo['detail']))

def delete_func(text, message):
    titlelist = db.get_list(message.body['channel'])
    if text in titlelist:
        db.del_memo(message.body['channel'], text)
        message.reply("メモを削除しました: {}".format(text))
    else:
        message.reply("そのようなメモは存在しません")

def list_func(message):
    memolist = db.get_list(message.body['channel'])
    if len(memolist) == 0:
        message.reply("保存されているメモはありません")
    else:
        titlelist = '\n'.join(memolist)
        message.reply("保存されているメモのリストです\n```{}```".format(titlelist))

def help_func(message):
    helplist = ["save タイトル(改行)内容", "load タイトル", "dele タイトル", "list", "help", \
                "チャンネルの場合は各コマンドの前に!を付けてください。", "すでに存在するタイトルでsaveした場合は上書きされます。"]
    helptext = "\n".join(helplist)
    message.reply("このボットの使い方です\n```{}```".format(helptext))