from .httpApi import RequestPasscode, RegisterDevice
import subprocess
import sys
import threading
import locale


def check_reg(
    user_id, user_pw, device_name="kakao.py", device_uuid="a2FrYW9weWRldjEyMDI="
):
    try:
        check_registered = input_timer(
            "If you are not registered yet, enter 'y' within 10 seconds: ", 10
        )
    except TimeoutError:
        check_registered = ""

    if check_registered != "y":
        return

    RequestPasscode(user_id, user_pw, device_name, device_uuid)

    print("Please check your phone or computer for the authorization passcode")
    passcode = input("PASSCODE: ")

    RegisterDevice(user_id, user_pw, device_name, device_uuid, passcode)
    # TODO: 성공 여부 체크
    print("Registered!")


def input_timer(prompt, timeout_sec):
    class Local:
        # check if timeout occured
        _timeout_occured = False

        def on_timeout(self, process):
            self._timeout_occured = True
            process.kill()
            # clear stdin buffer (for linux)
            # when some keys hit and timeout occured before enter key press,
            # that input text passed to next input().
            # remove stdin buffer.
            try:
                import termios

                termios.tcflush(sys.stdin, termios.TCIFLUSH)
            except ImportError:
                # windows, just exit
                pass

        def input_timer_main(self, prompt_in, timeout_sec_in):
            # print with no new line
            print(prompt_in, end="")

            # print prompt_in immediately
            sys.stdout.flush()

            # new python input process create.
            # and print it for pass stdout
            cmd = [sys.executable, "-c", "print(input())"]
            with subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            ) as proc:
                timer_proc = threading.Timer(timeout_sec_in, self.on_timeout, [proc])
                try:
                    # timer set
                    timer_proc.start()
                    stdout, stderr = proc.communicate()

                    # get stdout and trim new line character
                    result = stdout.decode(locale.getpreferredencoding()).strip("\r\n")
                finally:
                    # timeout clear
                    timer_proc.cancel()

            # timeout check
            if self._timeout_occured is True:
                # move the cursor to next line
                print("")
                raise TimeoutError
            return result

    t = Local()
    return t.input_timer_main(prompt, timeout_sec)
