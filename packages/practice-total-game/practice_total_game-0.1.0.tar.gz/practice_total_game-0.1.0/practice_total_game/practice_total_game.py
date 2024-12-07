import pygame
import math
import random

import os
import re
import random
from difflib import SequenceMatcher
import speech_recognition as sr
from tkinter import Tk, Label, Button, filedialog

import pygame
import math
import random
from kivy.base import runTouchApp
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image

import cv2
import numpy as np
from ultralytics import YOLO
import mediapipe as mp
import random
import os
from tkinter import Tk, Label, Button, Entry, filedialog, messagebox
from PIL import Image, ImageTk

import pytesseract
from PIL import Image
import re
import tkinter as tk
from tkinter import messagebox
import os
import shutil




class total_game:
    def __init__(self):
        pass

# -------------------------------------------Roulette.py-----------------------------------

    def initialize_pygame(self, width, height):
        pygame.init()
        screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Roulette")
        clock = pygame.time.Clock()
        return screen, clock

    def draw_roulette(self, screen, font, values, angle, width, height):
        screen.fill((60, 0, 0))  # Background color (brown)
        radius = min(width, height) // 2 - 40
        triangle_size = 15
        center = (width // 2, height // 2)

        colors = [(255, 0, 0), (0, 0, 0)]  # Red and Black for segments

        for i, value in enumerate(values):
            start_angle = math.radians(360 / len(values) * i + angle)
            end_angle = math.radians(360 / len(values) * (i + 1) + angle)
            color = colors[i % len(colors)]

            points = [center]
            num_points = 50
            for j in range(num_points + 1):
                t = j / num_points
                angle_step = start_angle + (end_angle - start_angle) * t
                x = center[0] + radius * math.cos(angle_step)
                y = center[1] + radius * math.sin(angle_step)
                points.append((x, y))
            pygame.draw.polygon(screen, color, points)

            text_angle = (start_angle + end_angle) / 2
            text_x = center[0] + radius * 0.7 * math.cos(text_angle)
            text_y = center[1] + radius * 0.7 * math.sin(text_angle)
            text_surface = font.render(value, True, (255, 255, 255))
            screen.blit(text_surface, (text_x - text_surface.get_width() // 2,
                                       text_y - text_surface.get_height() // 2))

        pygame.draw.circle(screen, (60, 0, 0), center, 10)

        pygame.draw.polygon(screen, (255, 255, 255), [
            (center[0], center[1] - radius + triangle_size),
            (center[0] - triangle_size, center[1] - radius),
            (center[0] + triangle_size, center[1] - radius)
        ])

    def get_result(self, values, angle):
        arrow_angle = (270 - angle) % 360
        index = int(arrow_angle // (360 / len(values)))
        return values[index]

    def roulette_game(self, values):
        width, height = 500, 500
        # Use self to call the initialize_pygame method
        screen, clock = self.initialize_pygame(width, height)
        font = pygame.font.SysFont("malgungothic", 20)

        angle = 0
        speed = 0
        is_spinning = False
        is_stopping = False

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if not is_spinning:
                        speed = random.uniform(10, 15)
                        is_spinning = True
                    elif not is_stopping:
                        is_stopping = True

            if is_spinning:
                angle += speed
                if is_stopping:
                    speed *= 0.98
                    if speed < 0.1:
                        speed = 0
                        is_spinning = False
                        is_stopping = False
                        result = self.get_result(values, angle)  # Use self
                        print(f"Selected value: {result}")

            self.draw_roulette(screen, font, values, angle, width, height)  # Use self
            pygame.display.flip()
            clock.tick(60)

        pygame.quit()



# -------------------------------------------Pronunciation.py----------------------------------- 


    def initialize_gui(self, root, width, height, bg_color):
        root.title("어려운 문장 발음 평가 프로그램")
        root.geometry(f"{width}x{height}")
        root.configure(bg=bg_color)

        return root


    def create_label(self, root, text, font, bg, fg, pady=0, wraplength=None, justify=None):
        label = Label(root, text=text, font=font, bg=bg, fg=fg, wraplength=wraplength, justify=justify)
        label.pack(pady=pady)
        return label


    def create_button(self, root, text, command, font, bg, fg, activebackground, width, height, pady=0):
        button = Button(
            root, text=text, command=command, font=font, bg=bg, fg=fg,
            activebackground=activebackground, relief="flat", width=width, height=height
        )
        button.pack(pady=pady)
        return button


    def select_sentence(self, sentences, sentence_label):
        selected_sentence = random.choice(sentences)
        sentence_label.config(text=selected_sentence)
        return selected_sentence


    def similar_sound_correction(self, word):
        replacements = {
            "쟝": "장",
            "깡": "강",
            "도로록": "도로룩",
            "두루룩": "두루륵",
            "홑겹": "홀겹",
            "겹홑": "겹홀",
            "창살": "창쌀",
            "단풍잎": "단퐁잎",
            "토끼통": "토끼톳",
            "쇠창살": "쇠쌍살",
            "철창살": "쓸창살",
            "공장장": "공쨍장"
        }
        for key, value in replacements.items():
            word = word.replace(key, value)
        return word


    def evaluate_pronunciation(self, correct_text, recorded_text):
        correct_words = re.findall(r'\S+', correct_text)
        recorded_words = re.findall(r'\S+', recorded_text)

        total_ratio = 0
        word_count = min(len(correct_words), len(recorded_words))
        detailed_results = []

        for correct_word, recorded_word in zip(correct_words, recorded_words):
            corrected_recorded_word = similar_sound_correction(recorded_word)
            ratio = SequenceMatcher(None, correct_word, corrected_recorded_word).ratio()
            detailed_results.append((correct_word, corrected_recorded_word, ratio))
            total_ratio += ratio

        avg_ratio = total_ratio / word_count if word_count > 0 else 0
        avg_percentage = avg_ratio * 100

        if avg_ratio > 0.9:
            result = "정확"
        elif avg_ratio > 0.7:
            result = "조금 틀림"
        else:
            result = "많이 틀림"

        return result, avg_percentage, detailed_results


    def recognize_audio(self, file_path):
        recognizer = sr.Recognizer()
        audio_file = sr.AudioFile(file_path)

        with audio_file as source:
            audio_data = recognizer.record(source)

        try:
            text = recognizer.recognize_google(audio_data, language='ko-KR')
            return text
        except sr.UnknownValueError:
            return "음성을 인식할 수 없습니다."
        except sr.RequestError:
            return "서비스에 접근할 수 없습니다."


    def analyze_pronunciation(self, correct_text, audio_file, result_label):
        recorded_text = recognize_audio(audio_file)
        print(f"녹음된 텍스트: {recorded_text}")

        result, avg_percentage, _ = evaluate_pronunciation(correct_text, recorded_text)
        print(f"발음 정확도: {result} (평균 유사도: {avg_percentage:.2f}%)")

        result_label.config(text=f"발음 정확도: {result} ({avg_percentage:.2f}%)")


    def upload_audio(self, selected_sentence, result_label):
        file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav;*.mp3")])
        if file_path:
            self.analyze_pronunciation(selected_sentence, file_path, result_label)


    def pronunciation_app(self):
        # Initialize GUI
        root = Tk()
        root = self.initialize_gui(root, width=800, height=500, bg_color="#FFFFFF")

        # Sentences for evaluation
        sentences = [
            "도토리가 문을 도로록, 드르륵, 두루룩 열었는가?",
            "우리집 옆집 앞집 뒤창살은 홑겹창살이고 우리집 뒷집 앞집 옆창살은 겹홑창살이다.",
            "한양양장점 옆에 한영양장점 한영양장점 옆에 한양양장점",
            "청단풍잎 홍단풍잎 흑단풍잎 백단풍잎",
            "작은 토끼 토끼통 옆에는 큰 토끼 토끼 통이 있고 큰 토끼 토끼통 옆에는 작은 토끼 토끼 통이 있다.",
            "생각이란 생각하면 생각할수록 생각나는 것이 생각이므로 생각하지 않는 생각이 좋은 생각이라 생각한다.",
            "앞뜰에 있는 말뚝이 말 맬 말뚝이냐 말 못맬 말뚝이냐",
            "경찰청 쇠창살 외철창살 검찰청 쇠창살 쌍철창살",
            "간장 공장 공장장은 강 공장장이고 된장 공장 공장장은 장 공장장이다."
        ]

        # GUI Elements
        label = self.create_label(
            root, "랜덤 문장을 읽어보세요!", font=("Arial", 18), bg="#FFFFFF", fg="#333333", pady=20
        )

        sentence_label = self.create_label(
            root, "", font=("Arial", 14), bg="#FFFFFF", fg="#333333", pady=20, wraplength=700, justify="center"
        )

        result_label = self.create_label(
            root, "", font=("Arial", 14), bg="#FFFFFF", fg="#333333", pady=30
        )

        def select_sentence_callback():
            nonlocal selected_sentence
            selected_sentence = self.select_sentence(sentences, sentence_label)

        def upload_audio_callback():
            self.upload_audio(selected_sentence, result_label)

        select_button = self.create_button(
            root, "누르면 랜덤한 문장이 나와요!", select_sentence_callback,
            font=("Arial", 14), bg="#87CEEB", fg="white",
            activebackground="#B0E0E6", width=23, height=2, pady=10
        )

        upload_button = self.create_button(
            root, "오디오 파일 업로드", upload_audio_callback,
            font=("Arial", 14), bg="#87CEEB", fg="white",
            activebackground="#B0E0E6", width=15, height=2, pady=10
        )

        # Initialize selected_sentence variable
        selected_sentence = ""

        root.mainloop()


# -------------------------------------------guess.py----------------------------------- 


    def guess_game_app(self, images):
        from kivy.uix.textinput import TextInput
        """Kivy Guess Game"""
        os.environ["KIVY_NO_ARGS"] = "0"
        os.environ.pop("KIVY_WINDOW", None)  # KIVY_WINDOW 설정 제거        
        # 상태 관리 변수
        current_index = [0]
        score = [0]

        # 레이아웃 설정
        root = FloatLayout()
        content = BoxLayout(orientation="vertical", size_hint=(0.8, 0.8), pos_hint={"center_x": 0.5, "center_y": 0.5})

        # 이미지 위젯
        image_widget = Image(source=images[current_index[0]]["image"], size_hint=(1, 0.6))
        content.add_widget(image_widget)

        # 텍스트 입력
        text_input = TextInput(
            hint_text="ENTER THE ANSWER",
            multiline=False,
            size_hint=(0.5, 0.1),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )
        content.add_widget(text_input)

        # 결과 메시지
        result_label = Label(text="", size_hint=(1, 0.2))
        content.add_widget(result_label)

        # 제출 버튼 이벤트 처리 함수
        def check_answer(instance):
            user_input = text_input.text.strip()
            correct_answer = images[current_index[0]]["answer"]

            if user_input == correct_answer:
                result_label.text = "GOOD!!!!"
                result_label.color = (0, 1, 0, 1)
                score[0] += 1
            else:
                result_label.text = f"Error! Answer is '{correct_answer}'!"
                result_label.color = (1, 0, 0, 1)

            # 다음 문제로 이동
            current_index[0] += 1
            if current_index[0] < len(images):
                image_widget.source = images[current_index[0]]["image"]
                text_input.text = ""
            else:
                result_label.text = f"GameOver! Score: {score[0]}/{len(images)}"
                text_input.disabled = True
                instance.disabled = True
                from kivy.app import App
                app = App.get_running_app()
                if app:
                    app.stop()

        # 제출 버튼
        submit_button = Button(
            text="Submit", size_hint=(0.5, 0.1), pos_hint={"center_x": 0.5, "center_y": 0.5}
        )
        submit_button.bind(on_press=check_answer)

        # 레이아웃 구성
        content.add_widget(submit_button)
        root.add_widget(content)

        # Kivy 애플리케이션 실행
        runTouchApp(root)


#-------------------------------image.py----------------------------------



    def initialize_gui(self, state):
        """GUI 초기화"""
        root = state["root"]
        root.title("Group Photo Analysis")
        root.geometry("500x600")

        Label(root, text="이미지 선택", font=("Arial", 14)).pack(pady=10)
        Button(root, text="이미지 선택", command=lambda: self.select_image(state)).pack()

        state["img_label"] = Label(root)
        state["img_label"].pack(pady=10)

        Label(root, text="벌칙 입력", font=("Arial", 14)).pack(pady=10)
        state["mission_entry"] = Entry(root, width=30)
        state["mission_entry"].pack(pady=5)

        Button(root, text="분석 시작", command=lambda: self.start_analysis(state)).pack(pady=20)


    def select_image(self, state):
        """이미지 파일 선택"""
        image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
        if image_path:
            state["image_path"] = image_path
            img = Image.open(image_path)
            img = img.resize((400, 300), Image.Resampling.LANCZOS)
            img = ImageTk.PhotoImage(img)
            state["img_label"].config(image=img)
            state["img_label"].image = img
            state["img_label"].text = image_path


    def start_analysis(self, state):
        """분석 시작"""
        if not state["image_path"]:
            messagebox.showerror("Error", "이미지를 선택하세요.")
            return

        mission = state["mission_entry"].get()
        if not mission:
            messagebox.showerror("Error", "벌칙을 입력하세요.")
            return

        self.analyze_group_photo(state, state["image_path"], mission)


    def analyze_group_photo(self, state, image_path, mission, confidence_threshold=0.5):
        """YOLO로 사람 감지 후 Mediapipe로 분석"""
        image = cv2.imread(image_path)
        if image is None:
            messagebox.showerror("Error", "이미지를 불러올 수 없습니다.")
            return

        model = state["model"]
        results = model(image)
        detections = results[0].boxes.data.cpu().numpy()

        people = [d for d in detections if int(d[5]) == 0 and d[4] >= confidence_threshold]
        all_features = []

        for idx, person in enumerate(people, start=1):
            x1, y1, x2, y2, _, _ = person
            x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
            person_image = image[y1:y2, x1:x2]
            features = self.analyze_person(person_image, idx)
            all_features.extend(features)
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(image, f"Person {idx}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        if all_features:
            selected_feature = random.choice(all_features)
            result_text = f"{selected_feature} : {mission}"
            messagebox.showinfo("Result", result_text)
        else:
            result_text = "감지된 특징이 없습니다."
            messagebox.showinfo("Result", result_text)

        cv2.waitKey(0)
        cv2.destroyAllWindows()


    def analyze_person(self, image_region, person_id):
        """개별 사람의 특징 분석"""
        features = []
        h, w, _ = image_region.shape

        # BGR 이미지를 RGB로 변환
        image_rgb = cv2.cvtColor(image_region, cv2.COLOR_BGR2RGB)

        # Mediapipe Hands 분석
        with mp.solutions.hands.Hands(static_image_mode=True, max_num_hands=2, min_detection_confidence=0.5) as hands:
            hand_results = hands.process(image_rgb)
            if hand_results.multi_hand_landmarks:
                for hand_landmarks in hand_results.multi_hand_landmarks:
                    thumb_tip = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.THUMB_TIP]
                    thumb_ip = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.THUMB_IP]
                    wrist = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.WRIST]

                    # 엄지손가락 감지: TIP이 IP보다 위에 있는 경우
                    if thumb_tip.y < thumb_ip.y and thumb_tip.y < wrist.y:
                        features.append(f"Person {person_id}: 엄지손가락을 올린 사람")

                    # 손가락 V 포즈 감지
                    index_tip = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP]
                    middle_tip = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.MIDDLE_FINGER_TIP]
                    if index_tip.y < middle_tip.y:  # 손가락으로 V 포즈
                        features.append(f"Person {person_id}: 손가락으로 V 포즈를 한 사람")

        return features


    def group_photo_analyzer_app(self):
        """그룹 사진 분석 앱 실행"""
        root = Tk()

        state = {
            "root": root,
            "image_path": None,
            "model": YOLO("yolov8m.pt"),
            "img_label": None,
            "mission_entry": None,
        }

        self.initialize_gui(state)
        root.mainloop()
    

#-----------------------------------------receipt.py-------------------------------------

    
    def receipt(self):
        """
        영수증 이미지에서 금액을 추출하고, 인원 수로 나누어 금액을 계산하는 모든 작업을 하나의 함수에서 처리하는 함수.
        """
        try:
            # Tkinter 메인 창 생성
            root = tk.Tk()
            root.title("영수증 나누기 계산기")

            # 이미지 경로 입력
            tk.Label(root, text="이미지 경로:").grid(row=0, column=0, padx=10, pady=10)
            image_path_entry = tk.Entry(root, width=30)
            image_path_entry.grid(row=0, column=1, padx=10, pady=10)

            # 인원 수 입력
            tk.Label(root, text="인원 수:").grid(row=1, column=0, padx=10, pady=10)
            num_people_entry = tk.Entry(root, width=10)
            num_people_entry.grid(row=1, column=1, padx=10, pady=10)

                    # Tesseract 경로 설정
            if shutil.which('tesseract'):  # 시스템 PATH에서 'tesseract' 실행 파일 찾기
                tesseract_path = shutil.which('tesseract')
            elif os.getenv('TESSERACT_PATH'):  # 환경 변수 TESSERACT_PATH 확인
                tesseract_path = os.getenv('TESSERACT_PATH')
            else:
                # 운영 체제에 따라 기본 경로 설정
                if os.name == 'nt':  # Windows
                    tesseract_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
                elif os.name == 'posix':  # Linux 또는 macOS
                    tesseract_path = '/usr/local/bin/tesseract'  # macOS / Linux
                else:
                    tesseract_path = None  # 경로를 찾을 수 없음

            if not tesseract_path or not os.path.isfile(tesseract_path):
                messagebox.showerror("에러", "Tesseract 경로를 찾을 수 없습니다. Tesseract가 설치되었는지 확인해 주세요.")
                return
            
            pytesseract.pytesseract.tesseract_cmd = tesseract_path


            def on_calculate_click():
                """
                계산 버튼 클릭 시 실행되는 함수.
                """
                image_path = image_path_entry.get()
                try:
                    num_people = int(num_people_entry.get())
                    
                    if num_people <= 0:
                        messagebox.showerror("에러", "인원 수는 1명 이상이어야 합니다.")
                        return

                    # 이미지에서 금액을 추출
                    img = Image.open(image_path)
                    result = pytesseract.image_to_string(img)

                    # 쉼표가 포함된 금액 추출
                    numbers_with_commas = re.findall(r'\d{1,3}(?:,\d{3})*', result)
                    numbers = [int(num.replace(',', '')) for num in numbers_with_commas]

                    # 가장 큰 금액 추출
                    total_amount = max(numbers) if numbers else None

                    if total_amount is not None:
                        # 1인당 금액 계산
                        amount_per_person = total_amount / num_people

                        # 금액 포맷팅
                        formatted_total = f"{total_amount:,} 원"
                        formatted_per_person = f"{amount_per_person:,.0f} 원"

                        # 결과 출력
                        result_text = f"총 금액: {formatted_total}\n1인당 금액: {formatted_per_person}"
                        messagebox.showinfo("계산 결과", result_text)
                    else:
                        messagebox.showerror("에러", "유효한 금액을 추출할 수 없습니다.")
                except Exception as e:
                    messagebox.showerror("에러", f"오류 발생: {e}")

            # 실행 버튼
            calculate_button = tk.Button(root, text="계산하기", command=on_calculate_click)
            calculate_button.grid(row=2, column=0, columnspan=2, pady=20)

            root.mainloop()
        
        except Exception as e:
            messagebox.showerror("에러", f"전체 프로그램 실행 중 오류 발생: {e}")


# from total_game import total_game

# if __name__ == "__main__":
#     tg = total_game()
#     tg.receipt()