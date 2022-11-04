from flask import Flask,send_from_directory,render_template,redirect,url_for,request,session
import mysql.connector
import random
import os

app=Flask(__name__)
app.secret_key="defaultkey"

@app.route("/catalogue")
def show_catalogue():
    with mysql.connector.connect(host="localhost",user="root",password="Sroot@1234",database="shopping_cart")as connection:
        with connection.cursor() as cursor:
            cursor.execute("select * from product;")
            result=cursor.fetchall()
            
            
    username=None
    if 'username' in session:
        username=session['username']
    print(session)
    page=render_template("catalogue.html",records=result,username=username)
    return page


@app.route("/")
def home_page():
    return redirect(url_for("show_catalogue"))
    
@app.route("/addtocart")
def addtocart():
    print(request.args)
    print(session)
    
    if 'username' not in session:
        return redirect(url_for("login"))
        
    if 'cart' not in session:
        session['cart']={}
        
    if request.args['product_id'] not in session['cart']:
        session['cart'][request.args['product_id']]=0
        
    session['cart'][request.args['product_id']]=session['cart'][request.args['product_id']]+1
    session.modified=True
    return redirect(url_for("show_catalogue"))
    

@app.route("/showcart")
def showcart():
    if 'username' not in session:
        return redirect(url_for("login"))
    if 'cart' not in session:
        session['cart']={}
    cart_total=0
    all_records=[]
    for product_id,product_count in session['cart'].items():
        product=get_product_from_database(product_id)
        if len(product)!=1:
            raise Exception(f"for product id{product_id} product count fetched from database is {len(product)}")
            
        a_product=product[0]
        record=list(a_product)+[product_count]
        del record[3]
        
        item_total=record[3]*record[4]
        record.append(item_total)
        cart_total=cart_total+item_total
        all_records.append(record)
        
    return render_template("show_cart.html",all_records=all_records,cart_total=cart_total,username=session['username'])
    
def get_product_from_database(product_id):
    query=f"""select * from product where id='{product_id}';"""
    with mysql.connector.connect(host="localhost",user="root",password="Sroot@1234",database="shopping_cart")as connection:
        with connection.cursor() as cursor:
            cursor.execute(query)
            result=cursor.fetchall()
            return result
            
        
@app.route("/ship_cart")
def ship_cart():
    all_records=[]
    cart_total=0
    
    for product_id,product_count in session['cart'].items():
        product=get_product_from_database(product_id)
        a_product=product[0]
        a_product=list(a_product)
        a_product[3]=a_product[3]- product_count
        update_product_inventory_count(a_product[0],a_product[3])
        
    session['cart']={}
    session.modified=True
    
    return render_template("show_cart.html",all_records=all_records,cart_total=cart_total,username=session['username'])
    
def update_product_inventory_count(product_id,inventory_count):
    with mysql.connector.connect(host="localhost",user="root",password="Sroot@1234",database="shopping_cart")as connection:
        with connection.cursor() as cursor:
            cursor.execute(f"""UPDATE product
                            SET inventory_quantity={inventory_count}
                            WHERE id='{product_id}';
                            """)
            connection.commit()

        
@app.route("/login",methods=["GET","POST"])
def login():
        if request.method=="GET":
            page=render_template("login.html")
            return page
        elif request.method=="POST":
            name=request.form['username']
            password=request.form['password']
            USERS=get_USER(name)
            
            if len(USERS)==0:
                page=render_template("login.html")
                return page
            elif len(USERS)>1:
                raise Exception(f"Multiple USERS with same name present")
            
            USER=USERS[0]
            if USER[2]==password:
                session['username']=request.form['username']
                return redirect(url_for("show_catalogue"))
            else:
                page=render_template("login.html")
                return page
                
def get_USER(name):
    with mysql.connector.connect(host="localhost",user="root",password="Sroot@1234",database="shopping_cart")as connection:
        with connection.cursor() as cursor:
            cursor.execute(f"""select * from USER where name='{name}';""")
            result=cursor.fetchall()
            return result


@app.route("/userregister",methods=["GET","POST"])
def userregister():
    id=str(random.randint(0,10000))
    if request.method=="GET":
        return render_template("userregister.html")
    elif request.method=="POST":
        name=request.form['username']
        password=request.form['password']
        email=request.form['email']
        USERS=get_USER(name)
        if len(USERS)>0:
            return render_template("userregister.html",already_exists=True)
        elif len(USERS)==0:
            with mysql.connector.connect(host="localhost",user="root",password="Sroot@1234",database="shopping_cart")as connection:
                with connection.cursor() as cursor:
                    cursor.execute(f"""insert into user(id,name,password,email)
                                    values('{id}','{name}','{password}','{email}');
                                    """)
                    connection.commit()
                    cursor.close()
                    session['name']=request.form['username']
                    session['password']=request.form['password']
                    session['email']=request.form['email']
                    return redirect(url_for('login'))
                    
                    
@app.route("/logout")
def logout():
    session.pop('username')
    return redirect(url_for("show_catalogue"))

@app.route('/static_pages/<path:file_name>')
def static_pages(file_name):
    return send_from_directory('static_pages',file_name)
    
if __name__=="__main__":
    app.run(host="0.0.0.0",port=50000)
