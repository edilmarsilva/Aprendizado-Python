import pyautogui
from time import sleep

# Abrir o EB
pyautogui.PAUSE = 1
pyautogui.alert('CONFIRMA ATUALIZAÇÃO AUTOMÁTICA?')

pyautogui.hotkey('winleft', 'd')
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
sleep(50)

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
pyautogui.doubleClick(x=44, y=352)
sleep(2)

# Abrir o ASBYTE / Logon / Usuarios
pyautogui.doubleClick(x=711, y=215)
sleep(3)
pyautogui.doubleClick(x=724, y=319)
sleep(3)
pyautogui.doubleClick(x=729, y=250)
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
