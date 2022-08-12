a_string = "A string is more than its parts!"
matches = ["more", "wholesome", "milk"]

if all(x in a_string for x in matches):
    print(1)



my_favorite_type = '''
卷积
深度学习
机器视觉
opencv
android
java
'''

print(my_favorite_type.split('\n')[1:-1])