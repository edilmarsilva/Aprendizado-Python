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
sleep(1)
pyautogui.press('enter')
sleep(10)

# Abrir SIAP 2 opção 6 e CONFIRMAR
pyautogui.press('6')
sleep(55)

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
sleep(1)
pyautogui.press('enter')
sleep(1)
pyautogui.press('enter')
sleep(3)
pyautogui.press('enter')

pyautogui.hotkey('winleft', 'd')



# 2 clics no SIAP PARTE 4
pyautogui.doubleClick(x=1313, y=234)
sleep(4)
# Abrir o C:
pyautogui.doubleClick(x=34, y=195)
sleep(2)
# IR até FTP
pyautogui.doubleClick(x=48, y=401)
sleep(2)

# Abrir o ASBYTE
pyautogui.doubleClick(x=718, y=216)
sleep(3)

# Abrir public_html
pyautogui.doubleClick(x=718, y=232)
sleep(3)

# Abrir logon
pyautogui.doubleClick(x=722, y=317)
sleep(3)

# Abrir usuários
pyautogui.doubleClick(x=713, y=248)
sleep(3)

# Selecionar todos arquivos
pyautogui.click(x=218, y=356)
pyautogui.hotkey('ctrl', 'a')

# Passar para direita
pyautogui.click(x=657, y=384)

# Sobrescrever ALL
pyautogui.click(x=617, y=428)
sleep(16)

# Sair do FTP
pyautogui.click(x=1316, y=64)
pyautogui.click(x=682, y=442)
