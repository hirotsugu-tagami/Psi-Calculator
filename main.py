# -*- coding: utf-8 -*-
"""
@author: Hirotsugu Tagami
@E-mail: hirotsugu@g.ecc.u-tokyo.ac.jp
 ver1.0: 2022/11/10
 ver2.0: 2025/08/21
"""

import sys
import math
import numpy as np
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QLineEdit, QComboBox, QPushButton, QGroupBox, 
                            QMessageBox, QFormLayout, QGridLayout)
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QFont, QDoubleValidator, QIntValidator

class CrystalPlaneAngleCalculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # ウィンドウの設定
        self.setWindowTitle('結晶面間角度計算')
        self.setGeometry(100, 100, 600, 650)
        
        # メインウィジェットとレイアウト
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        
        # 結晶系の選択
        crystal_system_layout = QHBoxLayout()
        self.main_layout.addLayout(crystal_system_layout)
        
        crystal_system_label = QLabel('結晶系:')
        crystal_system_label.setFont(QFont('Arial', 12))
        crystal_system_layout.addWidget(crystal_system_label)
        
        self.crystal_system_combo = QComboBox()
        self.crystal_system_combo.setFont(QFont('Arial', 12))
        self.crystal_system_combo.addItems(['立方晶', '正方晶', '直方晶', '六方晶', '三方晶', '単斜晶', '三斜晶'])
        self.crystal_system_combo.currentIndexChanged.connect(self.update_input_fields)
        crystal_system_layout.addWidget(self.crystal_system_combo)
        crystal_system_layout.addStretch()
        
        # 格子定数グループ
        lattice_group = QGroupBox('格子定数')
        lattice_group.setFont(QFont('Arial', 11))
        self.main_layout.addWidget(lattice_group)
        
        lattice_layout = QGridLayout(lattice_group)
        
        # 格子定数の入力フィールド
        # doubleeValidatorを作成
        double_validator = QDoubleValidator()
        double_validator.setNotation(QDoubleValidator.StandardNotation)
        
        # a, b, c
        lattice_layout.addWidget(QLabel('a [Å]:'), 0, 0)
        self.a_edit = QLineEdit('1.0')
        self.a_edit.setValidator(double_validator)
        self.a_edit.setFixedWidth(80)
        self.a_edit.textChanged.connect(self.sync_lattice_parameters)
        lattice_layout.addWidget(self.a_edit, 0, 1)
        
        lattice_layout.addWidget(QLabel('b [Å]:'), 1, 0)
        self.b_edit = QLineEdit('1.0')
        self.b_edit.setValidator(double_validator)
        self.b_edit.setFixedWidth(80)
        lattice_layout.addWidget(self.b_edit, 1, 1)
        
        lattice_layout.addWidget(QLabel('c [Å]:'), 2, 0)
        self.c_edit = QLineEdit('1.0')
        self.c_edit.setValidator(double_validator)
        self.c_edit.setFixedWidth(80)
        lattice_layout.addWidget(self.c_edit, 2, 1)
        
        # α, β, γ
        lattice_layout.addWidget(QLabel('α [°]:'), 0, 2)
        self.alpha_edit = QLineEdit('90.0')
        self.alpha_edit.setValidator(double_validator)
        self.alpha_edit.setFixedWidth(80)
        self.alpha_edit.textChanged.connect(self.sync_lattice_angles)
        lattice_layout.addWidget(self.alpha_edit, 0, 3)
        
        lattice_layout.addWidget(QLabel('β [°]:'), 1, 2)
        self.beta_edit = QLineEdit('90.0')
        self.beta_edit.setValidator(double_validator)
        self.beta_edit.setFixedWidth(80)
        lattice_layout.addWidget(self.beta_edit, 1, 3)
        
        lattice_layout.addWidget(QLabel('γ [°]:'), 2, 2)
        self.gamma_edit = QLineEdit('90.0')
        self.gamma_edit.setValidator(double_validator)
        self.gamma_edit.setFixedWidth(80)
        lattice_layout.addWidget(self.gamma_edit, 2, 3)

        # 格子定数の列をstretchさせる
        lattice_layout.setColumnStretch(1, 1)
        lattice_layout.setColumnStretch(3, 1)
        
        # 面指数グループ
        indices_group = QGroupBox('面指数')
        indices_group.setFont(QFont('Arial', 11))
        self.main_layout.addWidget(indices_group)
        
        indices_layout = QVBoxLayout(indices_group)
        
        # 整数用バリデータを作成
        int_validator = QIntValidator()
        
        # 第1面指数
        plane1_label = QLabel('第1面指数 (hkl):')
        plane1_label.setFont(QFont('Arial', 12))
        indices_layout.addWidget(plane1_label)
        
        plane1_layout = QHBoxLayout()
        indices_layout.addLayout(plane1_layout)
        
        plane1_layout.addWidget(QLabel('h:'))
        self.h1_edit = QLineEdit('1')
        self.h1_edit.setValidator(int_validator)
        self.h1_edit.setFixedWidth(60)
        plane1_layout.addWidget(self.h1_edit)
        
        plane1_layout.addWidget(QLabel('k:'))
        self.k1_edit = QLineEdit('0')
        self.k1_edit.setValidator(int_validator)
        self.k1_edit.setFixedWidth(60)
        plane1_layout.addWidget(self.k1_edit)
        
        plane1_layout.addWidget(QLabel('l:'))
        self.l1_edit = QLineEdit('0')
        self.l1_edit.setValidator(int_validator)
        self.l1_edit.setFixedWidth(60)
        plane1_layout.addWidget(self.l1_edit)
        
        plane1_layout.addStretch()
        
        # 第2面指数
        plane2_label = QLabel('第2面指数 (h\'k\'l\'):')
        plane2_label.setFont(QFont('Arial', 12))
        indices_layout.addWidget(plane2_label)
        
        plane2_layout = QHBoxLayout()
        indices_layout.addLayout(plane2_layout)
        
        plane2_layout.addWidget(QLabel('h\':'))
        self.h2_edit = QLineEdit('0')
        self.h2_edit.setValidator(int_validator)
        self.h2_edit.setFixedWidth(60)
        plane2_layout.addWidget(self.h2_edit)
        
        plane2_layout.addWidget(QLabel('k\':'))
        self.k2_edit = QLineEdit('1')
        self.k2_edit.setValidator(int_validator)
        self.k2_edit.setFixedWidth(60)
        plane2_layout.addWidget(self.k2_edit)
        
        plane2_layout.addWidget(QLabel('l\':'))
        self.l2_edit = QLineEdit('0')
        self.l2_edit.setValidator(int_validator)
        self.l2_edit.setFixedWidth(60)
        plane2_layout.addWidget(self.l2_edit)
        
        plane2_layout.addStretch()
        
        # 計算ボタン
        calc_button = QPushButton('角度を計算')
        calc_button.setFont(QFont('Arial', 12))
        calc_button.setFixedHeight(40)
        calc_button.clicked.connect(self.calculate_angle)
        self.main_layout.addWidget(calc_button)
        
        # 結果表示エリア
        result_group = QGroupBox('計算結果')
        result_group.setFont(QFont('Arial', 11))
        self.main_layout.addWidget(result_group)
        
        result_layout = QVBoxLayout(result_group)
        self.result_label = QLabel('')
        self.result_label.setFont(QFont('Arial', 12))
        self.result_label.setAlignment(Qt.AlignCenter)
        result_layout.addWidget(self.result_label)
        
        # 情報エリア
        info_group = QGroupBox('情報')
        info_group.setFont(QFont('Arial', 11))
        self.main_layout.addWidget(info_group)
        
        info_layout = QVBoxLayout(info_group)
        info_text = "このアプリケーションは結晶面間の角度を計算します。\n結晶系によって必要なパラメータが自動で入力されます。"
        info_label = QLabel(info_text)
        info_label.setFont(QFont('Arial', 11))
        info_layout.addWidget(info_label)
        
        # スペースを追加
        self.main_layout.addStretch()

        # フッター (コピーライト)
        copyright_label = QLabel("Copyright © 2022-2025 Hirotsugu Tagami. All Rights Reserved.")
        copyright_label.setFont(QFont('Arial', 9))
        copyright_label.setAlignment(Qt.AlignCenter)
        copyright_label.setStyleSheet("color: gray;")
        self.main_layout.addWidget(copyright_label)
        
        # 初期設定を適用
        self.update_input_fields()
        
        # ウィンドウを表示
        self.show()
    
    @pyqtSlot()
    def update_input_fields(self):
        # 入力フィールドを一度有効化
        self.a_edit.setEnabled(True)
        self.b_edit.setEnabled(True)
        self.c_edit.setEnabled(True)
        self.alpha_edit.setEnabled(True)
        self.beta_edit.setEnabled(True)
        self.gamma_edit.setEnabled(True)
        
        # 現在のa値を保存
        a_value = self.a_edit.text()
        
        # 結晶系によって入力を調整
        crystal_system = self.crystal_system_combo.currentText()
        
        if crystal_system == "立方晶":
            self.b_edit.setEnabled(False)
            self.c_edit.setEnabled(False)
            self.alpha_edit.setEnabled(False)
            self.beta_edit.setEnabled(False)
            self.gamma_edit.setEnabled(False)
            
            # 値をコピー
            self.b_edit.setText(a_value)
            self.c_edit.setText(a_value)
            
            # 角度を90度に設定
            self.alpha_edit.setText("90.0")
            self.beta_edit.setText("90.0")
            self.gamma_edit.setText("90.0")
            
        elif crystal_system == "正方晶":
            self.b_edit.setEnabled(False)
            self.alpha_edit.setEnabled(False)
            self.beta_edit.setEnabled(False)
            self.gamma_edit.setEnabled(False)
            
            # 値をコピー
            self.b_edit.setText(a_value)
            
            # 角度を90度に設定
            self.alpha_edit.setText("90.0")
            self.beta_edit.setText("90.0")
            self.gamma_edit.setText("90.0")
            
        elif crystal_system == "直方晶":
            self.alpha_edit.setEnabled(False)
            self.beta_edit.setEnabled(False)
            self.gamma_edit.setEnabled(False)
            
            # 角度を90度に設定
            self.alpha_edit.setText("90.0")
            self.beta_edit.setText("90.0")
            self.gamma_edit.setText("90.0")
            
        elif crystal_system == "六方晶":
            self.b_edit.setEnabled(False)
            self.alpha_edit.setEnabled(False)
            self.beta_edit.setEnabled(False)
            self.gamma_edit.setEnabled(False)
            
            # 値をコピー
            self.b_edit.setText(a_value)
            
            # 角度を設定
            self.alpha_edit.setText("90.0")
            self.beta_edit.setText("90.0")
            self.gamma_edit.setText("120.0")
            
        elif crystal_system == "三方晶":
            self.b_edit.setEnabled(False)
            self.c_edit.setEnabled(False)
            self.beta_edit.setEnabled(False)
            self.gamma_edit.setEnabled(False)
            
            # 値をコピー
            self.b_edit.setText(a_value)
            self.c_edit.setText(a_value)
            
            # 角度をコピー
            alpha_value = self.alpha_edit.text()
            self.beta_edit.setText(alpha_value)
            self.gamma_edit.setText(alpha_value)
            
        elif crystal_system == "単斜晶":
            self.alpha_edit.setEnabled(False)
            self.gamma_edit.setEnabled(False)
            
            # 角度を90度に設定
            self.alpha_edit.setText("90.0")
            self.gamma_edit.setText("90.0")
    
    @pyqtSlot(str)
    def sync_lattice_parameters(self, text):
        # 結晶系に応じてパラメータを同期
        crystal_system = self.crystal_system_combo.currentText()
        
        if crystal_system in ["立方晶", "正方晶", "六方晶"]:
            self.b_edit.setText(text)
            
        if crystal_system in ["立方晶", "三方晶"]:
            self.c_edit.setText(text)
    
    @pyqtSlot(str)
    def sync_lattice_angles(self, text):
        # 結晶系に応じて角度を同期
        crystal_system = self.crystal_system_combo.currentText()
        
        if crystal_system == "三方晶":
            self.beta_edit.setText(text)
            self.gamma_edit.setText(text)
    
    @pyqtSlot()
    def calculate_angle(self):
        try:
            # 格子定数の取得
            a = float(self.a_edit.text())
            b = float(self.b_edit.text())
            c = float(self.c_edit.text())
            alpha = math.radians(float(self.alpha_edit.text()))
            beta = math.radians(float(self.beta_edit.text()))
            gamma = math.radians(float(self.gamma_edit.text()))
            
            # 面指数の取得
            h1 = int(self.h1_edit.text())
            k1 = int(self.k1_edit.text())
            l1 = int(self.l1_edit.text())
            
            h2 = int(self.h2_edit.text())
            k2 = int(self.k2_edit.text())
            l2 = int(self.l2_edit.text())
            
            # 単位ベクトルのチェック
            if h1 == 0 and k1 == 0 and l1 == 0:
                raise ValueError("第1面指数が(0,0,0)です。有効な面指数を入力してください。")
            if h2 == 0 and k2 == 0 and l2 == 0:
                raise ValueError("第2面指数が(0,0,0)です。有効な面指数を入力してください。")
            
            # 計算が必要な行列を生成
            cos_alpha = math.cos(alpha)
            cos_beta = math.cos(beta)
            cos_gamma = math.cos(gamma)
            sin_alpha = math.sin(alpha)
            sin_beta = math.sin(beta)
            sin_gamma = math.sin(gamma)
            
            # 体積の計算
            V = a * b * c * math.sqrt(1 - cos_alpha**2 - cos_beta**2 - cos_gamma**2 + 2 * cos_alpha * cos_beta * cos_gamma)
            
            # G行列（逆格子テンソル）の計算
            g11 = (b * c * sin_alpha) ** 2 / V**2
            g22 = (a * c * sin_beta) ** 2 / V**2
            g33 = (a * b * sin_gamma) ** 2 / V**2
            g12 = a * b * c**2 * (cos_alpha * cos_beta - cos_gamma) / V**2
            g13 = a * b**2 * c * (cos_alpha * cos_gamma - cos_beta) / V**2
            g23 = a**2 * b * c * (cos_beta * cos_gamma - cos_alpha) / V**2
            
            # 逆格子ベクトルの内積
            numerator = g11 * h1 * h2 + g22 * k1 * k2 + g33 * l1 * l2 + \
                       g12 * (h1 * k2 + h2 * k1) + g13 * (h1 * l2 + h2 * l1) + g23 * (k1 * l2 + k2 * l1)
            
            d1 = math.sqrt(g11 * h1**2 + g22 * k1**2 + g33 * l1**2 + 2 * g12 * h1 * k1 + 2 * g13 * h1 * l1 + 2 * g23 * k1 * l1)
            d2 = math.sqrt(g11 * h2**2 + g22 * k2**2 + g33 * l2**2 + 2 * g12 * h2 * k2 + 2 * g13 * h2 * l2 + 2 * g23 * k2 * l2)
            
            denominator = d1 * d2
            
            cos_psi = numerator / denominator
            
            # -1から1の範囲に収める（計算誤差対策）
            if cos_psi > 1:
                cos_psi = 1
            elif cos_psi < -1:
                cos_psi = -1
                
            psi = math.degrees(math.acos(cos_psi))
            
            # 結果を表示
            self.result_label.setText(f"面 ({h1},{k1},{l1}) と ({h2},{k2},{l2}) の間の角度: {psi:.4f}°")
            
        except ValueError as e:
            QMessageBox.warning(self, "入力エラー", f"入力値が正しくありません: {str(e)}")
        except ZeroDivisionError:
            QMessageBox.warning(self, "計算エラー", "ゼロ除算が発生しました。入力を確認してください。")
        except Exception as e:
            QMessageBox.critical(self, "エラー", f"計算中にエラーが発生しました: {str(e)}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # より洗練された外観
    calculator = CrystalPlaneAngleCalculator()
    sys.exit(app.exec_())