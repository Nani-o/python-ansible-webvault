from flask import Flask, render_template, request
import os, tempfile, subprocess
app = Flask(__name__)

@app.route('/',methods = ['POST','GET'])
def vault():
    if request.method == 'POST':
      vault_password = request.form['vault']
      content = request.form['content']
      vault_password_file = tempfile.mktemp()
      open(vault_password_file, 'w').write(vault_password)
      command = ("ansible-vault", "encrypt", "--vault-password-file", vault_password_file, "--output", "-")
      echo = subprocess.Popen(('echo', content), stdout=subprocess.PIPE)
      output = subprocess.check_output((command), stdin=echo.stdout)
      os.remove(vault_password_file)
      vaulted = output.decode('utf-8').split('\n')
      return render_template('vaulted.html', vaulted = vaulted)
    else:
      return render_template('webvault.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
