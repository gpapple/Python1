class Student():
    def __init__(self,name,age):
        self.name =name
        self.age =age
        print("My name is %s,My age is %s" %(self.name,self.age))

    def talk(self):
        print('Hello,World')
stu1= Student("Kobe",39)
stu1.talk()

'''class Student():
    def __init__(self,name,score):
        self.name = name
        self.score = score
    def get_score(self):
        if self.score >= 90:
            return 'A'
        elif self.score >=60:
            return 'B'
        else:
            return 'C'
stu1 = Student('Lisa',98)
print(stu1.name,stu1.get_score())'''

'''class Screen():
    @property
    def width(self):
        return self._width
    @width.setter
    def width(self,value):
        if not isinstance(value,int):
            raise ValueError('width must be an integer!')
        if value < 0 or value >100:
            raise ValueError('width must between 0~100')
        self._width = value

        @property
        def height(self):
            return self._height
        @height.setter
        def height(self,value):
            if not isinstance(value,int):
                raise ValueError('height must be an interge!')
            if value < 0 or value > 100:
                raise ValueError('height must between 0~100')
            self._height = value

        @property
        def resolution(self):
            return self._width * self._height
s = Screen()
s.width = 10
s.height = 200

print(s.height)'''





