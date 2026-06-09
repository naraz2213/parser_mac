import time
import pyautogui
import keyboard
import subprocess
import os

print("🚀 АВТОКЛИКЕР (с добиранием остатков в конце)")
print("=" * 60)
print("1. Открой Telegram Desktop → канал → Участники")
print("2. Разверни окно на весь экран")
print("=" * 60)

# --- КАЛИБРОВКА ---
print("\n📌 КАЛИБРОВКА КООРДИНАТ")
print("👉 Наведи мышку на ПОЛЕ ПОИСКА (лупа) и нажми F5")
keyboard.wait('f5')
search_x, search_y = pyautogui.position()
print(f"✅ Поле поиска: ({search_x}, {search_y})")

print("👉 Наведи мышку на ИМЯ ПЕРВОГО участника в списке и нажми F6")
keyboard.wait('f6')
member_x, member_y = pyautogui.position()
print(f"✅ Первый участник: ({member_x}, {member_y})")

# --- КАРТИНКИ ---
screenshot_dir = "screenshots"
if not os.path.exists(screenshot_dir):
    os.makedirs(screenshot_dir)

qr_icon = f'{screenshot_dir}/qr_icon.png'
at_icon = f'{screenshot_dir}/at_icon.png'

print("\n📸 КАЛИБРОВКА КАРТИНОК")
print("👉 Открой профиль любого участника")
print("👉 Наведи мышку на QR-код и нажми F7")
keyboard.wait('f7')
x, y = pyautogui.position()
pyautogui.screenshot(qr_icon, region=(x-15, y-15, 30, 30))
print(f"✅ QR сохранён")

print("👉 Наведи мышку на символ @ (в поле юзернейма) и нажми F8")
keyboard.wait('f8')
x, y = pyautogui.position()
pyautogui.screenshot(at_icon, region=(x-5, y-8, 12, 16))
print(f"✅ @ сохранён")

print("👉 Закрой профиль (нажми Esc)")

# --- КАЛИБРОВКА ГРАНИЦ СПИСКА ---
print("\n📌 КАЛИБРОВКА ГРАНИЦ СПИСКА")
print("👉 Наведи мышку на ЛЕВЫЙ ВЕРХНИЙ УГОЛ списка участников и нажми F9")
keyboard.wait('f9')
list_left, list_top = pyautogui.position()
print(f"✅ Левый верхний угол: ({list_left}, {list_top})")

print("👉 Наведи мышку на ПРАВЫЙ НИЖНИЙ УГОЛ списка участников и нажми F10")
keyboard.wait('f10')
list_right, list_bottom = pyautogui.position()
print(f"✅ Правый нижний угол: ({list_right}, {list_bottom})")

# --- ОБЛАСТЬ ПОИСКА QR ---
search_region = (list_left, list_top, list_right - list_left, list_bottom - list_top)

# --- СБОР ---
all_usernames = set()
stop_flag = False
last_user = None
repeat_count = 0

def stop_scraping():
    global stop_flag
    stop_flag = True

keyboard.add_hotkey('f12', stop_scraping)

print("\n🚀 СБОР ЗАПУЩЕН (F12 - стоп)")
print("=" * 50)

no_progress = 0
last_count = 0

while not stop_flag:
    pyautogui.click(member_x, member_y)
    time.sleep(0.8)
    if stop_flag:
        break

    # 1. ИЩЕМ QR
    qr_pos = None
    try:
        qr_pos = pyautogui.locateOnScreen(qr_icon, confidence=0.5, region=search_region)
    except:
        pass

    if qr_pos:
        # 2. ИЩЕМ @ СЛЕВА ОТ QR
        at_region = (list_left, qr_pos.top - 50, qr_pos.left - list_left, 100)
        at_pos = None
        try:
            at_pos = pyautogui.locateOnScreen(at_icon, confidence=0.5, region=at_region)
        except:
            pass
        
        if at_pos:
            # 3. КЛИКАЕМ ПО @
            pyautogui.click(at_pos.left + 5, at_pos.top + 5)
            time.sleep(0.15)
            pyautogui.hotkey('ctrl', 'c')
            time.sleep(0.15)

            res = subprocess.run(['powershell', '-command', 'Get-Clipboard'], capture_output=True, text=True)
            name = res.stdout.strip()
            if name:
                if not name.startswith('@'):
                    name = f'@{name}'
                
                if name == last_user:
                    repeat_count += 1
                    if repeat_count >= 5:
                        print(f"  🔄 Достигнут конец, добираем остатки...")
                        # ДОБИРАЕМ ОСТАТКИ: 8 раз вниз
                        original_y = member_y
                        for step in range(1, 9):
                            member_y = original_y + (step * 30)  # смещаем вниз
                            pyautogui.click(member_x, member_y)
                            time.sleep(0.5)
                            
                            # Пробуем найти QR на новой позиции
                            qr_pos2 = None
                            try:
                                qr_pos2 = pyautogui.locateOnScreen(qr_icon, confidence=0.5, region=search_region)
                            except:
                                pass
                            
                            if qr_pos2:
                                at_region2 = (list_left, qr_pos2.top - 50, qr_pos2.left - list_left, 100)
                                at_pos2 = None
                                try:
                                    at_pos2 = pyautogui.locateOnScreen(at_icon, confidence=0.5, region=at_region2)
                                except:
                                    pass
                                
                                if at_pos2:
                                    pyautogui.click(at_pos2.left + 5, at_pos2.top + 5)
                                    time.sleep(0.15)
                                    pyautogui.hotkey('ctrl', 'c')
                                    time.sleep(0.15)
                                    
                                    res2 = subprocess.run(['powershell', '-command', 'Get-Clipboard'], capture_output=True, text=True)
                                    name2 = res2.stdout.strip()
                                    if name2:
                                        if not name2.startswith('@'):
                                            name2 = f'@{name2}'
                                        if name2 not in all_usernames:
                                            all_usernames.add(name2)
                                            print(f"  ✅ [{len(all_usernames)}] {name2} (добрали)")
                            
                            pyautogui.press('esc')
                            time.sleep(0.2)
                        
                        member_y = original_y
                        print(f"  📌 Сбор завершён")
                        stop_flag = True
                        break
                else:
                    repeat_count = 0
                    last_user = name
                
                if name not in all_usernames:
                    all_usernames.add(name)
                    print(f"  ✅ [{len(all_usernames)}] {name}")
                    no_progress = 0
                else:
                    no_progress += 1
            else:
                no_progress += 1
        else:
            no_progress += 1
    else:
        no_progress += 1

    pyautogui.press('esc')
    time.sleep(0.2)
    pyautogui.scroll(-117)
    time.sleep(0.3)

    if len(all_usernames) == last_count:
        no_progress += 1
    else:
        last_count = len(all_usernames)
        no_progress = 0

    if no_progress >= 8:
        print(f"  📌 Сбор завершён")
        break

with open('usernames.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(sorted(all_usernames)))

print(f"\n🎉 ГОТОВО! Всего: {len(all_usernames)}")
print(f"💾 Файл: usernames.txt")