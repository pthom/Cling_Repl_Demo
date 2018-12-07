import sys
import time
import subprocess

def send_letter(letter):
  # V1 : simple print
  sys.stdout.write(letter)
  sys.stdout.flush()

  # V2: Test with expect (apt-get install expect)
  # cmd = """echo 'send "{}"' | expect""".format(c)
  # subprocess.run(cmd, shell=True)

def write_line(line):
  delay_letter = 0.038
  delay_line = 0.6
  prompts = ["[DOCKER] /sources_docker > ", "[cling]$ "]
  if len(line) == 0:
    time.sleep(delay_line)
    send_letter("\n")
  is_prompt = False
  for prompt in prompts:
    if line.startswith(prompt):
      is_prompt = True
      rest = line[len(prompt):]
      if rest.startswith("?"):
        rest = rest[1:]
      for c in rest:
        send_letter(c)
        time.sleep(delay_letter)
  if is_prompt:
    time.sleep(delay_line)
    send_letter("\n")
  # if not is_prompt:
  #   print(line)

def simulate_keypresses_parse(content):
  lines = content.split("\n")
  for line in lines:
      write_line(line)

def simulate_keypresses(content):
  lines = content.split("\n")
  for line in lines:
    for c in line:
      send_letter(c)
      time.sleep(0.03)
    send_letter("\n")
    time.sleep(0.5)


if __name__ == "__main__":
  filename = sys.argv[1]
  with open(filename, "r") as f:
    content = f.read()
  simulate_keypresses_parse(content)
  # simulate_keypresses(content)


# A lancer comme ceci :
# echo "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n" \
# && sleep 3 &&\
# python Simulate_KeyPresses.py session.txt | tee /dev/tty | cling --std=c++14
