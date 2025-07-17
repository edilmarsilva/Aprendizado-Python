import pyautogui
from time import sleep

pyautogui.PAUSE = 1
pyautogui.alert('CONFIRMA ATUALIZAÇÃO AUTOMÁTICA?')

# Chamar área de trabalho
pyautogui.hotkey('winleft', 'd')

# Abrir o EB
pyautogui.doubleClick(x=1315, y=44)
sleep(1.5)

# Abrir Mão de Obra opção 3
pyautogui.press('3')

# Abrir Ordem de Produção opção 8
pyautogui.press('8')

# Abrir SIAP 1 opção 5 e CONFIRMAR
pyautogui.press('5')
sleep(6)
pyautogui.press('enter')
sleep(30)

# Abrir SIAP 2 opção 6 e CONFIRMAR
pyautogui.press('6')
sleep(100)

# Sair do EB
pyautogui.press('esc')
pyautogui.press('esc')
pyautogui.press('esc')
pyautogui.press('esc')

pyautogui.hotkey('winleft', 'd')


# Atualizando a parte 3
pyautogui.doubleClick(x=1311, y=129)
sleep(2)
pyautogui.press('enter')
sleep(2)
pyautogui.press('enter')
sleep(2)
pyautogui.press('enter')
sleep(8)
pyautogui.press('enter')

pyautogui.hotkey('winleft', 'd')



# 2 clics no SIAP PARTE 4 (FileZilla)
pyautogui.doubleClick(x=1316, y=230)
sleep(3.0)
# Abrir o Conexão rápida:
pyautogui.click(x=756, y=86)
sleep(1.0)
# Selecionar o embo1:
pyautogui.click(x=860, y=150)
sleep(3.5)
pyautogui.press('enter')
sleep(3.0)

# Abrir o public_hyml / Logon / Usuarios
pyautogui.doubleClick(x=778, y=289)
sleep(2)
pyautogui.doubleClick(x=773, y=379)
sleep(2)
pyautogui.doubleClick(x=803, y=379)
sleep(2)

# Selecionar todos arquivos
pyautogui.click(x=91, y=395)
pyautogui.hotkey('ctrl', 'a')

# Clicar com botão direito do mouse
pyautogui.rightClick(x=65, y=395)

# Selecionar UPLOAD
pyautogui.click(x=136, y=406)
sleep(0.5)
pyautogui.click(x=787, y=441)
sleep(0.5)
pyautogui.click(x=787, y=464)
sleep(0.5)
pyautogui.click(x=1086, y=496)

pyautogui.click(x=630, y=443)
sleep(0.5)
pyautogui.click(x=628, y=463)
sleep(0.5)
pyautogui.click(x=926, y=497)

sleep(30)
# Sair do FTP
pyautogui.click(x=1339, y=4)
