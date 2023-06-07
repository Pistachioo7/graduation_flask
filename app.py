from flask import Flask, jsonify, request, json
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_
import UserCF
import datetime


app = Flask(__name__) #构建一个flask应用
cors = CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@127.0.0.1:3306/graduation_thesis'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'this is a string'
db = SQLAlchemy(app)


class UserList(db.Model): #用户信息列表
    __tablename__ = 'users'
    uID = db.Column(db.Text, primary_key=True)
    uName = db.Column(db.Text)
    uSex = db.Column(db.Integer)
    uBirthday = db.Column(db.Date)
    uPassword = db.Column(db.Text)


class WindowList(db.Model): #食堂窗口列表
    __tablename__ = 'windows'
    wID = db.Column(db.Text, primary_key=True)
    wName = db.Column(db.Text)
    mealAmount = db.Column(db.Integer)
    wStatus = db.Column(db.Integer)
    wPassword = db.Column(db.Text)


class AdministratorList(db.Model): #管理员列表
    __tablename__ = 'administrators'
    aID = db.Column(db.Text, primary_key=True)
    aName = db.Column(db.Text)
    aPassword = db.Column(db.Text)


class MealList(db.Model): #餐品列表
    __tablename__ = 'meals'
    mID = db.Column(db.Text, primary_key=True)
    mName = db.Column(db.Text)
    wID = db.Column(db.Text)
    mType = db.Column(db.Text)
    mainIngredient = db.Column(db.Text)
    price = db.Column(db.Integer)
    maxSupply = db.Column(db.Integer)
    remainSupply = db.Column(db.Integer)


class OrderList(db.Model): #订单列表
    __tablename__ = 'orders'
    oID = db.Column(db.Text, primary_key=True)
    uID = db.Column(db.Text)
    wID = db.Column(db.Text)
    mID = db.Column(db.Text)
    oStatus = db.Column(db.Integer)
    oDatetime = db.Column(db.DateTime)
    fDatetime = db.Column(db.DateTime)


class AutoIncrement(db.Model): #oID自增
    __tablename__ = 'autoincrement'
    auID = db.Column(db.Text, primary_key=True)
    increment = db.Column(db.Text)


class RatingList(db.Model): #评分表
    __tablename__ = 'ratings'
    rID = db.Column(db.Text, primary_key=True)
    uID = db.Column(db.Text)
    mID = db.Column(db.Text)
    rating = db.Column(db.Integer)


@app.route('/getusers') #获取所有用户的信息
def getUsers():
    users = UserList.query.all() #查询所有用户信息
    # 数据类型转换
    user_list = []
    for user in users:
        user_list.append({'uID': user.uID, 'uName': user.uName, 'uSex': user.uSex,
                          'uBirthday': user.uBirthday, 'uPassword': user.uPassword})
    return jsonify(user_list)


@app.route('/getwindows') #获取所有窗口的信息
def getWindows():
    windows = WindowList.query.all() #查询所有窗口信息
    window_list = []
    for window in windows:
        window_list.append({'wID': window.wID, 'wName': window.wName, 'mealAmount': window.mealAmount,
                         'wStatus': window.wStatus, 'wPassword': window.wPassword})
    return jsonify(window_list)


@app.route('/getuserbyid/<string:user_id>') #按uID查找用户
def getUserByID(user_id):
    try:
        qUser = UserList.query.filter(UserList.uID == user_id)
        if len(qUser.all()) > 0:
            user = qUser.first()
            user_dict = {'uID': user.uID, 'uName': user.uName, 'uSex': user.uSex,
                         'uBirthday': user.uBirthday, 'uPassword': user.uPassword}
            return jsonify(user_dict)
        return jsonify({'status': 0})
    except:
        return jsonify({'status': 0})


@app.route('/getwindowbyid/<string:window_id>') #按wID查找窗口
def getWindowByID(window_id):
    try:
        qWindow = WindowList.query.filter(WindowList.wID == window_id)
        if len(qWindow.all()) > 0:
            window = qWindow.first()
            window_dict = {'wID': window.wID, 'wName': window.wName, 'mealAmount': window.mealAmount,
                         'wStatus': window.wStatus, 'wPassword': window.wPassword}
            return jsonify(window_dict)
        return jsonify({'status': 0})
    except:
        return jsonify({'status': 0})


@app.route('/getmealbyid/<string:meal_id>') #按mID查找餐品
def getMealByID(meal_id):
    try:
        qMeal = MealList.query.filter(MealList.mID == meal_id)
        if len(qMeal.all()) > 0:
            meal = qMeal.first()
            meal_dict = {'mID': meal.mID, 'mName': meal.mName, 'wID': meal.wID, 'mType': meal.mType,
                         'mainIngredient': meal.mainIngredient, 'price': meal.price, 'maxSupply': meal.maxSupply,
                         'remainSupply': meal.remainSupply}
            return jsonify(meal_dict)
        return jsonify({'status': 0})
    except:
        return jsonify({'status': 0})


@app.route('/getmealbyname/<string:meal_name>') #按名查找餐品
def getMealByName(meal_name):
    try:
        qMeal = MealList.query.filter(MealList.mName == meal_name)
        if len(qMeal.all()) > 0:
            meal = qMeal.first()
            meal_dict = {'mID': meal.mID, 'mName': meal.mName, 'wID': meal.wID, 'mType': meal.mType,
                         'mainIngredient': meal.mainIngredient, 'price': meal.price, 'maxSupply': meal.maxSupply,
                         'remainSupply': meal.remainSupply}
            return jsonify(meal_dict)
        return jsonify({'status': 0})
    except:
        return jsonify({'status': 0})


@app.route('/getadminbyid/<string:admin_id>') #按aID查找管理员
def getAdminByID(admin_id):
    try:
        qAdmin = AdministratorList.query.filter(AdministratorList.aID == admin_id)
        if len(qAdmin.all()) > 0:
            admin = qAdmin.first()
            admin_dict = {'aID': admin.aID, 'aName': admin.aName, 'aPassword': admin.aPassword}
            return jsonify(admin_dict)
        return jsonify({'status': 0})
    except:
        return jsonify({'status': 0})


@app.route('/getorderbyid/<string:order_id>') #按oID查找订单
def getOrderByID(order_id):
    try:
        qOrder = OrderList.query.filter(OrderList.oID == order_id)
        if len(qOrder.all()) > 0:
            order = qOrder.first()
            order_dict = {'oID': order.oID, 'uID': order.uID, 'wID': order.wID, 'mID': order.mID,
                              'oStatus': order.oStatus, 'oDatetime': order.oDatetime, 'fDatetime': order.fDatetime}
            return jsonify(order_dict)
        return jsonify({'status': 0})
    except:
        return jsonify({'status': 0})


@app.route('/adduser', methods = ["GET", "POST"]) #添加用户
def addUser():
    if request.method == 'POST':
        try:
            data = json.loads(request.get_data())
            data['uBirthday'] = datetime.datetime.strptime(data['uBirthday'][:10], '%Y-%m-%d')
            user = UserList(uID=data['uID'], uName=data['uName'], uSex=data['uSex'],
                            uBirthday=data['uBirthday'], uPassword=data['uPassword'])
            db.session.add(user)
            db.session.commit()
            user_dict = {'uID': user.uID, 'uName': user.uName, 'uSex': user.uSex,
                         'uBirthday': user.uBirthday, 'uPassword': user.uPassword}
            return jsonify(user_dict)
        except:
            return jsonify({'status': 0})
    else:
        return jsonify({'status': 'GET'})


@app.route('/addwindow', methods = ["GET", "POST"]) #添加窗口
def addWindow():
    if request.method == 'POST':
        try:
            data = json.loads(request.get_data())
            window = WindowList(wID=data['wID'], wName=data['wName'], mealAmount=data['mealAmount'],
                            wStatus=data['wStatus'], wPassword=data['wPassword'])
            db.session.add(window)
            db.session.commit()
            window_dict = {'wID': window.wID, 'wName': window.wName, 'mealAmount': window.mealAmount,
                         'wStatus': window.wStatus, 'wPassword': window.wPassword}
            return jsonify(window_dict)
        except:
            return jsonify({'status': 0})
    else:
        return jsonify({'status': 'GET'})


@app.route('/deleteuser/<string:user_id>', methods = ['GET', 'POST']) #删除用户信息
def deleteUser(user_id):
    if request.method == 'POST':
        user = UserList.query.filter(UserList.uID == user_id).first()
        db.session.delete(user)
        db.session.commit()
        return jsonify({'status': 1})
    else:
        return jsonify({'status': 'GET'})


@app.route('/deletewindow/<string:window_id>', methods = ['GET', 'POST']) #删除窗口信息
def deleteWindow(window_id):
    if request.method == 'POST':
        window = WindowList.query.filter(WindowList.wID == window_id).first()
        db.session.delete(window)
        db.session.commit()
        return jsonify({'status': 1})
    else:
        return jsonify({'status': 'GET'})


@app.route('/edituser/<string:user_id>', methods=['GET', 'POST']) #编辑用户信息
def editUser(user_id):
    if request.method == 'POST':
        data = json.loads(request.get_data())
        user = UserList.query.filter(UserList.uID == user_id).first()
        data['uBirthday'] = data['uBirthday'][:10]
        user.uName = data['uName']
        user.uSex = data['uSex']
        user.uBirthday = data['uBirthday']
        user.uPassword = data['uPassword']
        db.session.commit()
        return jsonify({'status': 1})
    else:
        return jsonify({'status': 'GET'})


@app.route('/editwindow/<string:window_id>', methods=['GET', 'POST']) #编辑窗口信息
def editWindow(window_id):
    if request.method == 'POST':
        data = json.loads(request.get_data())
        window = WindowList.query.filter(WindowList.wID == window_id).first()
        window.wName = data['wName']
        window.mealAmount = data['mealAmount']
        window.wStatus = data['wStatus']
        window.wPassword = data['wPassword']
        db.session.commit()
        return jsonify({'status': 1})
    else:
        return jsonify({'status': 'GET'})


@app.route('/editmeal/<string:meal_id>', methods=['GET', 'POST']) #编辑餐品信息
def editMeal(meal_id):
    if request.method == 'POST':
        data = json.loads(request.get_data())
        meal = MealList.query.filter(MealList.mID == meal_id).first()
        meal.uName = data['mName']
        meal.wID = data['wID']
        meal.mType = data['mType']
        meal.mainIngredient = data['mainIngredient']
        meal.price = data['price']
        meal.maxSupply = data['maxSupply']
        meal.remainSupply = data['remainSupply']
        db.session.commit()
        return jsonify({'status': 1})
    else:
        return jsonify({'status': 'GET'})


@app.route('/editorder/<string:order_id>', methods=['GET', 'POST']) #编辑订单状态
def editOrder(order_id):
    if request.method == 'POST':
        data = json.loads(request.get_data())
        order = OrderList.query.filter(OrderList.oID == order_id).first()
        order.oStatus = data['oStatus']
        db.session.commit()
        return jsonify({'status': 1})
    else:
        return jsonify({'status': 'GET'})


@app.route('/login', methods=['GET', 'POST']) #用户登录
def login():
    if request.method == 'POST':
        data = json.loads(request.get_data())
        id = data['uID']
        password = data['uPassword']
        qUser = UserList.query.filter(and_(UserList.uID == id, UserList.uPassword == password))
        if len(qUser.all()) > 0:
            return '1'
        else:
            return '0'
    else:
        return jsonify({'status': 'GET'})


@app.route('/windowlogin', methods=['GET', 'POST']) #窗口登录
def windowLogin():
    if request.method == 'POST':
        data = json.loads(request.get_data())
        id = data['wID']
        password = data['wPassword']
        qWindow = WindowList.query.filter(and_(WindowList.wID == id, WindowList.wPassword == password))
        if len(qWindow.all()) > 0:
            return '1'
        else:
            return '0'
    else:
        return jsonify({'status': 'GET'})


@app.route('/adminlogin', methods=['GET', 'POST']) #管理员登录
def adminLogin():
    if request.method == 'POST':
        data = json.loads(request.get_data())
        id = data['aID']
        password = data['aPassword']
        qAdmin = AdministratorList.query.filter(and_(AdministratorList.aID == id, AdministratorList.aPassword == password))
        if len(qAdmin.all()) > 0:
            return '1'
        else:
            return '0'
    else:
        return jsonify({'status': 'GET'})


@app.route('/getmeals') #获取所有餐品的信息
def getMeals():
    meals = MealList.query.all() #查询所有餐品信息
    # 数据类型转换
    meal_list = []
    for meal in meals:
        meal_list.append({'mID': meal.mID, 'mName': meal.mName, 'wID': meal.wID, 'mType': meal.mType,
                         'mainIngredient': meal.mainIngredient, 'price': meal.price, 'maxSupply': meal.maxSupply,
                         'remainSupply': meal.remainSupply})
    return jsonify(meal_list)


@app.route('/getcurrentorders/<string:user_id>') #获取用户的当前订单
def getCurrentOrders(user_id):
    qOrders = OrderList.query.filter(and_(OrderList.uID == user_id, OrderList.oStatus.in_({0, 1, 2}))) #查询用户当前订单
    if len(qOrders.all()) > 0:
        orders = qOrders.all()
        order_list = []
        for order in orders:
            order_list.append({'oID': order.oID, 'uID': order.uID, 'wID': order.wID, 'mID': order.mID,
                              'oStatus': order.oStatus, 'oDatetime': order.oDatetime, 'fDatetime': order.fDatetime})
        return jsonify(order_list)
    else:
        order_list = []
        return jsonify(order_list)


@app.route('/getreceivedorders/<string:window_id>') #获取窗口的当前订单
def getReceivedOrders(window_id):
    qOrders = OrderList.query.filter(and_(OrderList.wID == window_id, OrderList.oStatus.in_({0, 1, 2}))) #查询窗口当前订单
    if len(qOrders.all()) > 0:
        orders = qOrders.all()
        order_list = []
        for order in orders:
            order_list.append({'oID': order.oID, 'uID': order.uID, 'wID': order.wID, 'mID': order.mID,
                              'oStatus': order.oStatus, 'oDatetime': order.oDatetime, 'fDatetime': order.fDatetime})
        return jsonify(order_list)
    else:
        order_list = []
        return jsonify(order_list)


@app.route('/addmeal', methods = ["GET", "POST"]) #新增餐品
def addMeal():
    if request.method == 'POST':
        try:
            data = json.loads(request.get_data())
            meal = MealList(mID=data['mID'], mName=data['mName'], wID=data['wID'], mType=data['mType'],
                            mainIngredient=data['mainIngredient'], price=data['price'], maxSupply=data['maxSupply'],
                            remainSupply=data['remainSupply'])
            window = WindowList.query.filter(WindowList.wID == meal.wID).first()
            window.mealAmount += 1
            db.session.add(meal)
            db.session.commit()
            meal_dict = {'mID': meal.mID, 'mName': meal.mName, 'wID': meal.wID, 'mType': meal.mType,
                         'mainIngredient': meal.mainIngredient, 'price': meal.price, 'maxSupply': meal.maxSupply,
                         'remainSupply': meal.remainSupply}
            return jsonify(meal_dict)
        except:
            return jsonify({'status': 0})
    else:
        return jsonify({'status': 'GET'})


@app.route('/deletemeal/<string:meal_id>', methods = ['GET', 'POST']) #撤销餐品
def deleteMeal(meal_id):
    if request.method == 'POST':
        meal = MealList.query.filter(MealList.mID == meal_id).first()
        window = WindowList.query.filter(WindowList.wID == meal.wID).first()
        window.mealAmount -= 1
        db.session.delete(meal)
        db.session.commit()
        return jsonify({'status': 1})
    else:
        return jsonify({'status': 'GET'})


@app.route('/order', methods=['GET', 'POST']) #订餐
def order():
    if request.method == 'POST':
        data = json.loads(request.get_data())
        meal = MealList.query.filter(MealList.mID == data['mID']).first()
        meal.remainSupply -= 1
        order_id = AutoIncrement.query.filter(AutoIncrement.auID == '0').first().increment
        order = OrderList(oID=order_id, uID=data['uID'], wID=data['wID'], mID=data['mID'], oStatus=0,
                              oDatetime=datetime.datetime.now(), fDatetime=None)
        AutoIncrement.query.filter(AutoIncrement.auID == '0').update({'increment': str(int(order_id) + 1)})
        db.session.add(order)
        db.session.commit()
        return order_id
    else:
        return jsonify({'status': 'GET'})


@app.route('/searchorders/<string:user_id>') #按uID查询订单
def searchOrders(user_id):
    qOrder = OrderList.query.filter(OrderList.uID == user_id)
    if len(qOrder.all()) > 0:
        orders = qOrder.all()
        order_list = []
        for order in orders:
            order_list.append({'oID': order.oID, 'uID': order.uID, 'wID': order.wID, 'mID': order.mID,
                              'oStatus': order.oStatus, 'oDatetime': order.oDatetime, 'fDatetime': order.fDatetime})
        return jsonify(order_list)
    else:
        return '0'


@app.route('/cancelorder/<string:order_id>', methods = ['GET', 'POST']) #取消订单
def cancelOrder(order_id):
    if request.method == 'POST':
        order = OrderList.query.filter(OrderList.oID == order_id).first()
        order.fDatetime = datetime.datetime.now()
        meal_id = order.mID
        meal = MealList.query.filter(MealList.mID == meal_id).first()
        meal.remainSupply += 1
        order.oStatus = 4
        db.session.commit()
        return jsonify({'status': 1})
    else:
        return jsonify({'status': 'GET'})


@app.route('/checkorder/<string:order_id>', methods = ['GET', 'POST']) #接收订单
def checkOrder(order_id):
    if request.method == 'POST':
        order = OrderList.query.filter(OrderList.oID == order_id).first()
        order.oStatus = 1
        db.session.commit()
        return jsonify({'status': 1})
    else:
        return jsonify({'status': 'GET'})


@app.route('/cookorder/<string:order_id>', methods = ['GET', 'POST']) #订单备好
def cookOrder(order_id):
    if request.method == 'POST':
        order = OrderList.query.filter(OrderList.oID == order_id).first()
        order.oStatus = 2
        db.session.commit()
        return jsonify({'status': 1})
    else:
        return jsonify({'status': 'GET'})


@app.route('/finishorder/<string:order_id>', methods = ['GET', 'POST']) #完成订单
def finishOrder(order_id):
    if request.method == 'POST':
        order = OrderList.query.filter(OrderList.oID == order_id).first()
        order.oStatus = 3
        order.fDatetime = datetime.datetime.now()
        db.session.commit()
        return jsonify({'status': 1})
    else:
        return jsonify({'status': 'GET'})


@app.route('/getorders') #获取所有订单信息
def getOrders():
    orders = OrderList.query.all()
    order_list = []
    for order in orders:
        order_list.append({'oID': order.oID, 'uID': order.uID, 'wID': order.wID, 'mID': order.mID,
                              'oStatus': order.oStatus, 'oDatetime': order.oDatetime, 'fDatetime': order.fDatetime})
    return jsonify(order_list)


@app.route('/getuserorders/<string:user_id>') #获取用户历史订单信息
def getUserOrders(user_id):
    orders = OrderList.query.filter(OrderList.uID == user_id).all()
    order_list = []
    for order in orders:
        order_list.append({'oID': order.oID, 'uID': order.uID, 'wID': order.wID, 'mID': order.mID,
                              'oStatus': order.oStatus, 'oDatetime': order.oDatetime, 'fDatetime': order.fDatetime})
    return jsonify(order_list)


@app.route('/getwindoworders/<string:window_id>') #获取窗口历史订单信息
def getWindowOrders(window_id):
    orders = OrderList.query.filter(OrderList.wID == window_id).all()
    order_list = []
    for order in orders:
        order_list.append({'oID': order.oID, 'uID': order.uID, 'wID': order.wID, 'mID': order.mID,
                              'oStatus': order.oStatus, 'oDatetime': order.oDatetime, 'fDatetime': order.fDatetime})
    return jsonify(order_list)


@app.route('/getwindowmeals/<string:window_id>') #获取窗口餐品信息
def getWindowMeals(window_id):
    meals = MealList.query.filter(MealList.wID == window_id).all()
    meal_list = []
    for meal in meals:
        meal_list.append({'mID': meal.mID, 'mName': meal.mName, 'wID': meal.wID, 'mType': meal.mType,
                         'mainIngredient': meal.mainIngredient, 'price': meal.price, 'maxSupply': meal.maxSupply,
                         'remainSupply': meal.remainSupply})
    return jsonify(meal_list)


@app.route('/deleteorder/<string:order_id>', methods = ['GET', 'POST']) #删除订单
def deleteOrder(order_id):
    if request.method == 'POST':
        order = OrderList.query.filter(OrderList.oID == order_id).first()
        db.session.delete(order)
        db.session.commit()
        return jsonify({'status': 1})
    else:
        return jsonify({'status': 'GET'})


@app.route('/getratings') #获取所有评分信息
def getRatings():
    ratings = RatingList.query.all()
    rating_list = []
    for rating in ratings:
        rating_list.append({'uID': rating.uID, 'mID': rating.mID, 'rating': rating.rating})
    return jsonify(rating_list)


@app.route('/searchrating/<string:user_id>/<string:meal_id>') #查询评分
def searchRating(user_id, meal_id):
    qr = RatingList.query.filter(and_(RatingList.uID == user_id, RatingList.mID == meal_id))
    if len(qr.all()) > 0:
        rating = qr.first()
        return jsonify(rating.rating)
    else:
        return jsonify(-1)


@app.route('/rate', methods = ["GET", "POST"]) #评分
def rate():
    if request.method == 'POST':
        try:
            data = json.loads(request.get_data())
            rating_id = AutoIncrement.query.filter(AutoIncrement.auID == '1').first().increment
            rating = RatingList(rID=rating_id, uID=data['uID'], mID=data['mID'], rating=data['rating'])
            AutoIncrement.query.filter(AutoIncrement.auID == '1').update({'increment': str(int(rating_id) + 1)})
            db.session.add(rating)
            db.session.commit()
            rating_dict = {'uID': rating.uID, 'mID': rating.mID, 'rating': rating.rating}
            return jsonify(rating_dict)
        except:
            return jsonify({'status': 0})
    else:
        return jsonify({'status': 'GET'})


@app.route('/recommend/<string:user_id>') #推荐
def recommend(user_id):
    res = UserCF.run(user_id)
    print(res)
    meals_id = res['mID']
    meal_list = []
    for i in meals_id:
        meal = MealList.query.filter(MealList.mID == i).first()
        meal_list.append({'mID': meal.mID, 'mName': meal.mName, 'wID': meal.wID, 'mType': meal.mType,
                         'mainIngredient': meal.mainIngredient, 'price': meal.price, 'maxSupply': meal.maxSupply,
                         'remainSupply': meal.remainSupply})
    return jsonify(meal_list)


if __name__ == '__main__':
    app.run()
