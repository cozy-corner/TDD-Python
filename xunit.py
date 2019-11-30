class TestCase:
  def __init__(self, name):
    self.name = name

  # Javaのabstract
  def setUp(self):
    pass

  # Javaのabstract 
  def tearDown(self):
    pass

  def run(self):

    # TemplateMethod

    # 準備
    self.setUp()
    # getattr 組み込み関数
    # (x, 'foobar') は x.foobar と等価
    # Plugddable Object (リフレクション)
    method = getattr(self, self.name)
    method()
    
    # 後片付け
    self.tearDown()


# テスト対象クラス
class WasRun(TestCase):

  # 準備
  def setUp(self):
    self.log = "setUp "
  
  def testMethod(self):
    self.log = self.log + "testMethod "

  def tearDown(self):
    self.log = self.log + "tearDown "



class TestCaseTest(TestCase):

  def testTemplateMethod(self):
    test = WasRun("testMethod")
    test.run()
    assert("setUp testMethod tearDown " == test.log)

TestCaseTest("testTemplateMethod").run()

