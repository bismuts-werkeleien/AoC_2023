import sys, re

DIGIT_MAP = {
  'one': '1',
  'two': '2',
  'three': '3',
  'four': '4',
  'five': '5',
  'six': '6',
  'seven': '7',
  'eight': '8',
  'nine': '9'
}

with open(sys.argv[1], "r") as file:
    cal_vals = [value.strip("\n") for value in file]

# print(cal_vals)
#build number literals to digit
def build_digit(s):
    if s.isdigit():
        return s
    return DIGIT_MAP[s]

# sum up first and last cal_val
digits = 0
for i in cal_vals:
    t = [
      build_digit(x)
      # (?=...) lookahead assertion
      for x in re.findall(
        rf'(?=([1-9]|{"|".join(DIGIT_MAP.keys())}))',
        i
      )
    ]
    digit = t[0] + t[-1]
    d = int(digit)
    # print(digit)
    digits += d

print(f"Sum of calibration values: {digits}")

