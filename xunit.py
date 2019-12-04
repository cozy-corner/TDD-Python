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
    
    def run(self):
        result = TestResult()
        result.testStarted()

        # TemplateMethod

        # 準備
        self.setUp()
        # getattr 組み込み関数
        # (x, 'foobar') は x.foobar と等価
        # Plugddable Object (リフレクション)
        try:
            method = getattr(self, self.name)
            
            # 書籍ではこの代入はなし
            # 再帰の結果を保持していなかったため、errorCountが反映されなかった
            method_result = method()
            if isinstance(method_result, TestResult):
                result = method_result

        except:
            result.testFailed()

        # 後片付け
        self.tearDown()
        return result

# テスト対象クラス
class WasRun(TestCase):

    # 準備
    def setUp(self):
        self.log = "setUp "
    def testMethod(self):
        self.log = self.log + "testMethod "        
    def testBrokenMethod(self):
        raise Exception
    def tearDown(self):
        self.log = self.log + "tearDown "

class TestCaseTest(TestCase):

    # 正しい順序で実行されたことを検証
    def testTemplateMethod(self):
        test = WasRun("testMethod")
        test.run()
        assert("setUp testMethod tearDown " == test.log)

    # 正常パターン
    def testResult(self):
        test = WasRun("testMethod")
        result = test.run()
        assert("1 run, 0 failed" == result.summary())
        # 書籍ではこのreturn はなし
        return result

    # 例外
    def testFailedResult(self):
        test = WasRun("testBrokenMethod")
        result = test.run()
        assert("1 run, 1 failed" == result.summary())
        # 書籍ではこのreturn はなし
        return result

    # 失敗
    def testFailedResultFormatting(self):
        result = TestResult()
        result.testStarted()
        result.testFailed()
        assert("1 run, 1 failed" == result.summary())
        # 書籍ではこのreturn はなし
        return result

print(TestCaseTest("testTemplateMethod").run().summary())
print(TestCaseTest("testResult").run().summary())
print(TestCaseTest("testFailedResult").run().summary())
print(TestCaseTest("testFailedResultFormatting").run().summary())

# 書籍通りの実行結果
# 1 run, 0 failed
# 1 run, 0 failed
# 1 run, 0 failed
# 1 run, 0 failed

# 実行結果
# 1 run, 0 failed
# 1 run, 0 failed
# 1 run, 1 failed
# 1 run, 1 failed