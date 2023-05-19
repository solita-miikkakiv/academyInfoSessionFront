import json
import os
import org.parosproxy.paros.network.HttpRequestHeader as HttpRequestHeader
import org.parosproxy.paros.network.HttpHeader as HttpHeader
import org.zaproxy.zap.extension.script.ScriptVars as GlobalVariables
import org.parosproxy.paros.network.HttpMessage as HttpMessage
import org.parosproxy.paros.network.HtmlParameter as HtmlParameter
from org.apache.commons.httpclient import URI
 
import java.util.concurrent.TimeUnit as TimeUnit
import org.parosproxy.paros.control.Control as Control
import org.zaproxy.zap.extension.selenium.ExtensionSelenium as ExtensionSelenium
import org.openqa.selenium.By as By
import time
import threading
import org.openqa.selenium.chrome.ChromeDriver as ChromeDriver
import org.openqa.selenium.firefox.FirefoxDriver as FirefoxDriver
import org.openqa.selenium.firefox.FirefoxOptions as FirefoxOptions
import org.openqa.selenium.JavascriptExecutor as JavascriptExecutor
import org.openqa.selenium.WebElement as WebElement
from synchronize import make_synchronized

BASE_URL = os.getenv('ZAP_BASE_URL')
USER = os.getenv('ZAP_MS_USER')
PASS = os.getenv('ZAP_MS_PASSWORD')
 
# function called for every outgoing request (part of httpsender)
def sendingRequest(msg, initiator, helper):
    print('sendingRequest called for url=' + msg.getRequestHeader().getURI().toString())
 
    #checking if we already have an access token
    accessToken = GlobalVariables.getGlobalVar("accessToken")    
    if accessToken is not None:
        if isTokenValid(accessToken, helper) == True:
            setAccessTokenInHttpMessage(accessToken, msg)
            return
 
    accessToken = refreshAccessToken(helper)
    setAccessTokenInHttpMessage(accessToken, msg)
    return
 
#we have to make this function synchronized as we do not want to have duplicate concurrent attempts to login
@make_synchronized
def refreshAccessToken(helper):
    accessToken = GlobalVariables.getGlobalVar("accessToken")    
    if accessToken is not None and isTokenValid(accessToken, helper) == True:
        return accessToken
 
    GlobalVariables.setGlobalVar("accessToken", None)
    accessToken = doLogin(helper)
    GlobalVariables.setGlobalVar("accessToken", str(accessToken)) 
    return accessToken
 
def isTokenValid(accessToken, helper):
    authCheckUrl = BASE_URL + AUTH_ENDPOINT
    returnedMsg = callGet(helper, authCheckUrl, accessToken)
    print("Token valid:" + str(returnedMsg))
    return returnedMsg

 
#SIGN IN 
def doLogin(helper):
    print("attempt login")
    firefoxOptions = FirefoxOptions()
    firefoxOptions.addArguments("--window-size=1920,1080")
    firefoxOptions.addArguments("--disable-gpu")
    firefoxOptions.addArguments("--disable-extensions")
    firefoxOptions.addArguments("--proxy-server='direct://'")
    firefoxOptions.addArguments("--proxy-bypass-list=*")
    firefoxOptions.addArguments("--start-maximized")
    firefoxOptions.addArguments("--headless")
    webDriver = FirefoxDriver(firefoxOptions)
    webDriver.get(BASE_URL)
 
    # Open browser and navigate to root
    webDriver.get(BASE_URL)

    time.sleep(1)

    # Fill email field and click
    webDriver.findElement(By.id("username")).sendKeys(USER)
    webDriver.findElement(By.id("password")).sendKeys(PASS)

    time.sleep(2)

    # Handle "Stay signed in" button
    e = webDriver.findElement(By.id("login-button"))
    click(e, webDriver)
    time.sleep(4)
    print("login successful")
    
    accessToken = getAccessToken(webDriver)
    webDriver.close()
    return accessToken
 
def click(ele, webDriver):
    webDriver.executeScript("arguments[0].click()", ele)
 
# get token from localStorage
def getAccessToken(webDriver):
    localStorageItem = webDriver.executeScript("return localStorage.getItem('jwt')")

    token = str(localStorageItem)

    return token
 
 
# function called for every incoming server response
def responseReceived(msg, initiator, helper):
    pass
 
# function to make generic GET request
def callGet(helper, requestUrl, accessToken):
    print("attempt auth")
    firefoxOptions = FirefoxOptions()
    firefoxOptions.addArguments("--window-size=1920,1080")
    firefoxOptions.addArguments("--disable-gpu")
    firefoxOptions.addArguments("--disable-extensions")
    firefoxOptions.addArguments("--proxy-server='direct://'")
    firefoxOptions.addArguments("--proxy-bypass-list=*")
    firefoxOptions.addArguments("--start-maximized")
    firefoxOptions.addArguments("--headless")
    webDriver = FirefoxDriver(firefoxOptions)
    webDriver.get(requestUrl)

    time.sleep(2)

    try:
        webDriver.findElement(By.id("welcome"))
        webDriver.close()
        return True
    except:
        webDriver.close()
        return False
 
# function to set the token in Authorization header and in cookie in request
def setAccessTokenInHttpMessage(accessToken, msg):
    # print "setting token in request"
    msg.getRequestHeader().setHeader("Authorization", "Bearer " + accessToken)
    #cookie = HtmlParameter(HtmlParameter.Type.cookie, "token", accessToken)
    #cookies = msg.getRequestHeader().getCookieParams()
    #cookies.add(cookie)
    #msg.getRequestHeader().setCookieParams(cookies)
