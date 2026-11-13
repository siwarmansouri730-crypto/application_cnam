import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector


# --- 1. CONNEXION À LA BASE DE DONNÉES XAMPP ---
try:
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="cnam_db"
    )
    cursor = mydb.cursor()
    print("Connexion réussie !")
except mysql.connector.Error as err:
    print(f"Erreur : {err}")
    cursor = None
class CNAMConnectApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CNAM Connect - Portail Digital Assuré")
        self.root.geometry("1150x700")
        self.root.configure(bg="#F1F5F9")
        
        # الألوان الرسمية للمشروع
        self.DARK_BLUE = "#0B2545"
        self.PRIMARY_BLUE = "#134074"
        self.LIGHT_BLUE = "#8DA9C4"
        self.ACCENT_ORANGE = "#EE6C4D"
        self.GREEN_BG = "#2E7D32"
        self.BG_COLOR = "#F1F5F9"
        
        self.current_tab = "login"
        self.previous_tab = None

        self.create_login_screen()

    # -------------------------------------------------------------
    # 1. شاشة الدخول (LOGIN SCREEN)
    # -------------------------------------------------------------
    def create_login_screen(self):
        self.clear_window()
        self.current_tab = "login"

        login_frame = tk.Frame(self.root, bg=self.DARK_BLUE)
        login_frame.pack(fill="both", expand=True)

        card = tk.Frame(login_frame, bg="white", highlightthickness=1, highlightbackground="#E2E8F0")
        card.place(relx=0.5, rely=0.5, anchor="center", width=420, height=500)

        # اللوجو والعنوان
        logo_box = tk.Label(card, text="CNAM", font=("Segoe UI", 20, "bold"), bg=self.PRIMARY_BLUE, fg="white", width=6, height=2)
        logo_box.pack(pady=(25, 5))

        title = tk.Label(card, text="CNAM Connect", font=("Segoe UI", 18, "bold"), bg="white", fg=self.DARK_BLUE)
        title.pack()

        subtitle = tk.Label(card, text="الصندوق الوطني للتأمين على المرض - بوابة الخدمات", font=("Arial", 9), bg="white", fg="#64748B")
        subtitle.pack(pady=(0, 20))

        # الخانات (فارغة ليدخل المستخدم بياناته)
        form_frame = tk.Frame(card, bg="white")
        form_frame.pack(fill="x", padx=35)

        lbl_mat = tk.Label(form_frame, text="Matricule CNAM (المعرف الوحيد):", font=("Segoe UI", 9, "bold"), bg="white", fg="#334155")
        lbl_mat.pack(anchor="w", pady=(5, 2))
        self.ent_mat = tk.Entry(form_frame, font=("Segoe UI", 11), bd=1, relief="solid", justify="center")
        self.ent_mat.pack(fill="x", ipady=6, pady=(0, 10))
        self.ent_mat.insert(0, "12345678-01")

        lbl_cin = tk.Label(form_frame, text="N° CIN / Pass (كلمة السر):", font=("Segoe UI", 9, "bold"), bg="white", fg="#334155")
        lbl_cin.pack(anchor="w", pady=(5, 2))
        self.ent_cin = tk.Entry(form_frame, font=("Segoe UI", 11), show="*", bd=1, relief="solid", justify="center")
        self.ent_cin.pack(fill="x", ipady=6, pady=(0, 20))
        self.ent_cin.insert(0, "09876543")

        # زر الدخول
        btn_login = tk.Button(form_frame, text="Se Connecter / دخول", font=("Segoe UI", 11, "bold"), bg=self.PRIMARY_BLUE, fg="white", activebackground="#0B2545", activeforeground="white", bd=0, cursor="hand2", command=self.perform_login)
        btn_login.pack(fill="x", ipady=8)

    def perform_login(self):
        mat = self.ent_mat.get().strip()
        cin = self.ent_cin.get().strip()

        if not mat or not cin:
            messagebox.showwarning("تنبيه", "Veuillez saisir votre Matricule CNAM et votre CIN pour vous connecter.")
            return

        self.build_main_app()

    # -------------------------------------------------------------
    # 2. الواجهة الرئيسية (MAIN APP WORKSPACE)
    # -------------------------------------------------------------
    def build_main_app(self):
        self.clear_window()

        # الشريط العلوي
        self.header = tk.Frame(self.root, bg=self.DARK_BLUE, height=55)
        self.header.pack(fill="x", side="top")

        brand_lbl = tk.Label(self.header, text="  CNAM Connect  |  Centre Mohamed V", font=("Segoe UI", 11, "bold"), bg=self.DARK_BLUE, fg="white")
        brand_lbl.pack(side="left", padx=15)

        user_lbl = tk.Label(self.header, text="👤 Siwar Mansouri  ● Carnet Vert    ", font=("Segoe UI", 9, "bold"), bg=self.DARK_BLUE, fg="#A7F3D0")
        user_lbl.pack(side="right")

        btn_logout = tk.Button(self.header, text="Déconnexion", font=("Segoe UI", 9, "bold"), bg="#EF4444", fg="white", bd=0, padx=10, pady=3, cursor="hand2", command=self.create_login_screen)
        btn_logout.pack(side="right", padx=10)

        # حاوي التطبيق الأساسي
        self.body_frame = tk.Frame(self.root, bg=self.BG_COLOR)
        self.body_frame.pack(fill="both", expand=True)

        # القائمة الجانبية (Sidebar)
        self.sidebar = tk.Frame(self.body_frame, bg="#0F172A", width=230)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # محتوى الصفحات
        self.content_area = tk.Frame(self.body_frame, bg=self.BG_COLOR)
        self.content_area.pack(side="right", fill="both", expand=True, padx=20, pady=15)

        self.build_sidebar_menu()
        self.switch_to_tab("dashboard")

    def build_sidebar_menu(self):
        lbl_menu = tk.Label(self.sidebar, text="MENU PRINCIPAL", font=("Segoe UI", 8, "bold"), bg="#0F172A", fg="#64748B")
        lbl_menu.pack(anchor="w", padx=15, pady=(15, 5))

        nav_items = [
            ("🏠  Tableau de Bord", "dashboard"),
            ("💰  Remboursements (BS)", "remboursements"),
            ("🏥  Prises en Charge", "prises_en_charge"),
            ("🩺  Guide Médical", "doctors"),
            ("💳  Carte LABESS QR", "card"),
            ("💬  المراسلات والإشعارات", "messages")
        ]

        self.nav_buttons = {}
        for text, tab_key in nav_items:
            btn = tk.Button(self.sidebar, text=text, font=("Segoe UI", 9, "bold"), bg="#0F172A", fg="#94A3B8", activebackground=self.PRIMARY_BLUE, activeforeground="white", anchor="w", bd=0, padx=15, pady=10, cursor="hand2", command=lambda k=tab_key: self.switch_to_tab(k))
            btn.pack(fill="x")
            self.nav_buttons[tab_key] = btn

        # تنبيه انتهاء الدفتر في القائمة الجانبية
        alert_box = tk.Frame(self.sidebar, bg="#FEF3C7", highlightthickness=1, highlightbackground="#FCD34D")
        alert_box.pack(side="bottom", fill="x", padx=10, pady=10)
        
        tk.Label(alert_box, text="⚠️ Notification Carnet", font=("Segoe UI", 9, "bold"), bg="#FEF3C7", fg="#92400E").pack(anchor="w", padx=5, pady=(5,0))
        tk.Label(alert_box, text="Carnet de soin valide.\nExpiration dans 20 jours.", font=("Segoe UI", 8), bg="#FEF3C7", fg="#B45309", justify="left").pack(anchor="w", padx=5, pady=5)

    def create_top_bar(self, title_text, arabic_sub):
        top_bar = tk.Frame(self.content_area, bg="white", highlightthickness=1, highlightbackground="#E2E8F0")
        top_bar.pack(fill="x", pady=(0, 15), ipady=8, padx=5)

        if self.previous_tab and self.current_tab != "dashboard":
            btn_back = tk.Button(top_bar, text="⬅ Retour / الرجوع", font=("Segoe UI", 9, "bold"), bg="#E2E8F0", fg="#1E293B", bd=0, padx=12, pady=4, cursor="hand2", command=self.go_back)
            btn_back.pack(side="left", padx=10)

        lbl_title = tk.Label(top_bar, text=f"{title_text}  ({arabic_sub})", font=("Segoe UI", 11, "bold"), bg="white", fg=self.DARK_BLUE)
        lbl_title.pack(side="left", padx=10)

    def go_back(self):
        if self.previous_tab:
            target = self.previous_tab
            self.previous_tab = None
            self.switch_to_tab(target)

    def switch_to_tab(self, tab_key):
        if self.current_tab != tab_key:
            self.previous_tab = self.current_tab
            self.current_tab = tab_key

        for k, btn in self.nav_buttons.items():
            if k == tab_key:
                btn.config(bg=self.PRIMARY_BLUE, fg="white")
            else:
                btn.config(bg="#0F172A", fg="#94A3B8")

        for child in self.content_area.winfo_children():
            child.destroy()

        if tab_key == "dashboard":
            self.render_dashboard()
        elif tab_key == "remboursements":
            self.render_remboursements()
        elif tab_key == "prises_en_charge":
            self.render_prises_en_charge()
        elif tab_key == "doctors":
            self.render_doctors()
        elif tab_key == "card":
            self.render_card()
        elif tab_key == "messages":
            self.render_messages()

    # -------------------------------------------------------------
    # صفحات التطبيق (PAGES)
    # -------------------------------------------------------------
    def render_dashboard(self):
        self.create_top_bar("Tableau de Bord Principal", "الرئيسية")

        grid_frame = tk.Frame(self.content_area, bg=self.BG_COLOR)
        grid_frame.pack(fill="x", pady=(0, 15))

        # السقف السنوي
        card1 = tk.Frame(grid_frame, bg="#047857", padx=15, pady=15)
        card1.pack(side="left", fill="both", expand=True, padx=5)

        tk.Label(card1, text="Plafond Annuel (السقف السنوي 2026)", font=("Segoe UI", 9, "bold"), bg="#047857", fg="#A7F3D0").pack(anchor="w")
        tk.Label(card1, text="180 DT Restants", font=("Segoe UI", 15, "bold"), bg="#047857", fg="white").pack(anchor="w", pady=5)
        
        progress = ttk.Progressbar(card1, value=40, maximum=100)
        progress.pack(fill="x", pady=5)
        tk.Label(card1, text="Consommé: 120 DT  |  Max: 300 DT", font=("Segoe UI", 8, "bold"), bg="#047857", fg="#D1FAE5").pack(anchor="w")

        # إيداع ورقة علاج
        card2 = tk.Frame(grid_frame, bg="white", padx=15, pady=15, highlightthickness=1, highlightbackground="#E2E8F0")
        card2.pack(side="left", fill="both", expand=True, padx=5)

        tk.Label(card2, text="📄 Déposer un Bulletin de Soin", font=("Segoe UI", 10, "bold"), bg="white", fg=self.DARK_BLUE).pack(anchor="w")
        tk.Label(card2, text="تعبئة وإيداع ورقة علاج أونلاين", font=("Arial", 8), bg="white", fg="#64748B").pack(anchor="w", pady=(0, 8))
        
        btn_bs = tk.Button(card2, text="+ Soumettre un BS en Ligne", font=("Segoe UI", 9, "bold"), bg=self.ACCENT_ORANGE, fg="white", bd=0, pady=5, cursor="hand2", command=self.open_bs_modal)
        btn_bs.pack(fill="x", pady=(5, 0))

        # ملخص الحساب
        card3 = tk.Frame(grid_frame, bg="white", padx=15, pady=15, highlightthickness=1, highlightbackground="#E2E8F0")
        card3.pack(side="left", fill="both", expand=True, padx=5)

        tk.Label(card3, text="Identifiant Assuré", font=("Segoe UI", 8, "bold"), bg="white", fg="#94A3B8").pack(anchor="w")
        tk.Label(card3, text="Matricule: 12345678-01", font=("Segoe UI", 10, "bold"), bg="white", fg="#1E293B").pack(anchor="w")
        tk.Label(card3, text="Centre: Mohamed V Tunis", font=("Segoe UI", 8), bg="white", fg="#64748B").pack(anchor="w")
        tk.Label(card3, text="Carnet Actif ✅", font=("Segoe UI", 8, "bold"), bg="#DBEAFE", fg="#1E40AF", padx=8, pady=2).pack(anchor="w", pady=(8, 0))

        # التحديثات الأخيرة
        act_frame = tk.Frame(self.content_area, bg="white", padx=15, pady=15, highlightthickness=1, highlightbackground="#E2E8F0")
        act_frame.pack(fill="both", expand=True)

        tk.Label(act_frame, text="📋 Dernières Mises à Jour (التحديثات الأخيرة)", font=("Segoe UI", 11, "bold"), bg="white", fg=self.DARK_BLUE).pack(anchor="w", pady=(0, 10))

        item1 = tk.Frame(act_frame, bg="#F8FAFC", padx=10, pady=8, highlightthickness=1, highlightbackground="#E2E8F0")
        item1.pack(fill="x", pady=4)
        tk.Label(item1, text="✓  Bulletin de Soin #45821  -  Consultation Généraliste", font=("Segoe UI", 9, "bold"), bg="#F8FAFC", fg="#0F172A").pack(side="left")
        tk.Label(item1, text="Remboursé (45 DT) ✅", font=("Segoe UI", 9, "bold"), bg="#D1FAE5", fg="#065F46", padx=8, pady=2).pack(side="right")

    def render_remboursements(self):
        self.create_top_bar("Suivi des Remboursements", "استرجاع المصاريف")
        btn_new = tk.Button(self.content_area, text="+ Soumettre un Nouveau BS en Ligne", font=("Segoe UI", 9, "bold"), bg=self.ACCENT_ORANGE, fg="white", bd=0, pady=6, cursor="hand2", command=self.open_bs_modal)
        btn_new.pack(anchor="e", pady=(0, 15))

        card_bs1 = tk.Frame(self.content_area, bg="white", padx=15, pady=15, highlightthickness=1, highlightbackground="#10B981")
        card_bs1.pack(fill="x", pady=5)
        tk.Label(card_bs1, text="Bulletin de Soin #45821 - Consultation + Médicaments", font=("Segoe UI", 10, "bold"), bg="white", fg="#1E293B").pack(anchor="w")
        tk.Label(card_bs1, text="Status: Remboursé (45.000 DT)  |  Virement le: 15 Octobre 2026", font=("Segoe UI", 9), bg="white", fg="#059669").pack(anchor="w", pady=(3, 0))

    def render_prises_en_charge(self):
        self.create_top_bar("Demandes de Prise en Charge", "التكفل المباشر والموافقات")
        card_pc1 = tk.Frame(self.content_area, bg="white", padx=15, pady=15, highlightthickness=1, highlightbackground="#3B82F6")
        card_pc1.pack(fill="x", pady=5)
        tk.Label(card_pc1, text="Demande IRM / Scanner  (Dossier N°: PC-2026-889)", font=("Segoe UI", 10, "bold"), bg="white", fg="#1E293B").pack(anchor="w")
        tk.Label(card_pc1, text="Établissement: Clinique L'Espoir Tunis  |  Accordé jusqu'au: 30 Novembre 2026", font=("Segoe UI", 9), bg="white", fg="#2563EB").pack(anchor="w", pady=(3, 0))

    def render_doctors(self):
        self.create_top_bar("Médecins & Pharmacies Conventionnés", "دليل المتعاقدين")
        doc1 = tk.Frame(self.content_area, bg="white", padx=12, pady=12, highlightthickness=1, highlightbackground="#E2E8F0")
        doc1.pack(fill="x", pady=5)
        tk.Label(doc1, text="🩺 Dr. Mohamed El Hedi Tounsi  - Médecin de Famille", font=("Segoe UI", 10, "bold"), bg="white", fg="#1E293B").pack(anchor="w")
        tk.Label(doc1, text="📍 Av. Mohamed V, Tunis  |  Conventionné Tiers Payant", font=("Segoe UI", 8), bg="white", fg="#64748B").pack(anchor="w")

    def render_card(self):
        self.create_top_bar("Carte Digital LABESS", "بطاقة العلاج الرقمية")
        card_box = tk.Frame(self.content_area, bg="white", padx=25, pady=25, highlightthickness=2, highlightbackground=self.PRIMARY_BLUE)
        card_box.pack(anchor="center", pady=20)

        tk.Label(card_box, text="🔳", font=("Segoe UI", 48), bg="white").pack()
        tk.Label(card_box, text="Siwar Mansouri", font=("Segoe UI", 14, "bold"), bg="white", fg="#1E293B").pack()
        tk.Label(card_box, text="Matricule CNAM: 12345678-01", font=("Segoe UI", 10), bg="white", fg="#64748B").pack(pady=(0, 10))
        tk.Label(card_box, text="✅ Carnet Actif (Droits Ouverts 2026)", font=("Segoe UI", 9, "bold"), bg="#D1FAE5", fg="#065F46", padx=12, pady=4).pack()

    def render_messages(self):
        self.create_top_bar("المراسلات والإشعارات الرسمية", "Support & Messages")
        chat_frame = tk.Frame(self.content_area, bg="white", padx=15, pady=15, highlightthickness=1, highlightbackground="#E2E8F0")
        chat_frame.pack(fill="both", expand=True)

        self.chat_logs = tk.Text(chat_frame, font=("Segoe UI", 10), bg="#F8FAFC", bd=1, relief="solid", state="disabled")
        self.chat_logs.pack(fill="both", expand=True, pady=(0, 10))
        self.add_chat_message("CNAM Agent: مرحباً بكِ سوار في خدمة المراسلات المباشرة لمركز الكنام (شارع محمد الخامس). كيف يمكننا مساعدتكِ اليوم؟")

        input_box = tk.Frame(chat_frame, bg="white")
        input_box.pack(fill="x")
        self.chat_entry = tk.Entry(input_box, font=("Segoe UI", 10), bd=1, relief="solid")
        self.chat_entry.pack(side="left", fill="x", expand=True, ipady=6, padx=(0, 5))

        btn_send = tk.Button(input_box, text="إرسال", font=("Segoe UI", 9, "bold"), bg=self.PRIMARY_BLUE, fg="white", bd=0, padx=15, cursor="hand2", command=self.send_chat)
        btn_send.pack(side="right")

    def add_chat_message(self, text):
        self.chat_logs.config(state="normal")
        self.chat_logs.insert("end", text + "\n\n")
        self.chat_logs.see("end")
        self.chat_logs.config(state="disabled")

    def send_chat(self):
        msg = self.chat_entry.get().strip()
        if msg:
            self.add_chat_message(f"Vous (سوار): {msg}")
            self.chat_entry.delete(0, "end")
            self.root.after(1000, lambda: self.add_chat_message("CNAM Agent: Votre message a été transmis à l'agent CNAM du centre Mohamed V."))

    def open_bs_modal(self):
        win = tk.Toplevel(self.root)
        win.title("Déposer un BS en Ligne")
        win.geometry("400x300")
        win.configure(bg="white")
        win.grab_set()

        tk.Label(win, text="Déposer un Bulletin de Soin (BS)", font=("Segoe UI", 11, "bold"), bg="white", fg=self.DARK_BLUE).pack(pady=15)
        tk.Label(win, text="Numéro du Bulletin (BS):", font=("Segoe UI", 9, "bold"), bg="white").pack(anchor="w", padx=25)
        e_num = tk.Entry(win, font=("Segoe UI", 10), bd=1, relief="solid")
        e_num.pack(fill="x", padx=25, pady=(0, 10))

        tk.Label(win, text="Nom du Médecin / Établissement:", font=("Segoe UI", 9, "bold"), bg="white").pack(anchor="w", padx=25)
        e_doc = tk.Entry(win, font=("Segoe UI", 10), bd=1, relief="solid")
        e_doc.pack(fill="x", padx=25, pady=(0, 15))

        def submit():
            if e_num.get() and e_doc.get():
                messagebox.showinfo("Succès", "Votre Bulletin de Soin a été transmis avec succès !")
                win.destroy()
            else:
                messagebox.showwarning("Erreur", "Veuillez remplir tous les champs.")

        tk.Button(win, text="Envoyer au Centre CNAM", font=("Segoe UI", 10, "bold"), bg=self.ACCENT_ORANGE, fg="white", bd=0, pady=8, cursor="hand2", command=submit).pack(fill="x", padx=25)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = CNAMConnectApp(root)
    root.mainloop()