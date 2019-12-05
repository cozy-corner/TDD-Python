# テスト結果を保持するクラス
class TestResult:
    def __init__(self):
        self.runCount = 0
        self.errorCount = 0
    def testStarted(self):
        self.runCount = self.runCount + 1
    def testFailed(self):
        self.errorCount = self.errorCount + 1
    def summary(self):
        return "%d run, %d failed" % (self.runCount, self.errorCount)

class TestCase:
    def __init__(self, name):
        self.name = name

    # Javaのabstract
    def setUp(self):
        pass
    # Javaのabstract 
    def tearDown(self):
        pass
    
    def run(self, result):
        result.testStarted()

        # TemplateMethod

        # 準備
        self.setUp()
        # getattr 組み込み関数
        # (x, 'foobar') は x.foobar と等価
        # Plugddable Object (リフレクション)
        try:
            method = getattr(self, self.name)
            method()
        except Exception as e:
            print(e.args)
            result.testFailed()

        # 後片付け
        self.tearDown()

# テスト対象クラス
class WasRun(TestCase):

    # 準備
    def setUp(self):
        self.log = "setUp "
    def testMethod(self):
        self.log = self.log + "testMethod "        
    def testBrokenMethod(self):
        raise Exception('testBrokenMethod')
    def tearDown(self):
        self.log = self.log + "tearDown "

class TestCaseTest(TestCase):

    def setUp(self):
        self.result = TestResult()

    # 正しい順序で実行されたことを検証
    def testTemplateMethod(self):
        test = WasRun("testMethod")
        test.run(self.result)
        assert("setUp testMethod tearDown " == test.log)

    # 正常パターン
    def testResult(self):
        test = WasRun("testMethod")
        test.run(self.result)
        assert("1 run, 0 failed" == self.result.summary())

    # 例外
    def testFailedResult(self):
        test = WasRun("testBrokenMethod")
        test.run(self.result)
        assert("1 run, 1 failed" == self.result.summary())

    # 失敗
    def testFailedResultFormatting(self):
        self.result.testStarted()
        self.result.testFailed()
        assert("1 run, 1 failed" == self.result.summary())

    def testSuite(self):
        suite = TestSuite()
        suite.add(WasRun("testMethod"))
        suite.add(WasRun("testBrokenMethod"))
        suite.run(self.result)
        assert("2 run, 1 failed" == self.result.summary())

class TestSuite:
    def __init__(self):
        self.tests = []
    def add(self, test):
        self.tests.append(test)

    # まとめてテストを実行
    def run(self, result):
        for test in self.tests:
            test.run(result)

suite = TestSuite()
suite.add(TestCaseTest("testTemplateMethod"))
suite.add(TestCaseTest("testResult"))
suite.add(TestCaseTest("testFailedResult"))
suite.add(TestCaseTest("testFailedResultFormatting"))
suite.add(TestCaseTest("testSuite"))
result = TestResult()
suite.run(result)
print(result.summary())

# 実行結果
# 5 run, 0 failed
# 0 failed なのは、「想定通りに失敗した」という意味なので suite の結果としては問題ない