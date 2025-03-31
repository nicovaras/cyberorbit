## 📄 PDF: Topic 3 – Subtopic: File Upload Vulnerabilities  
**Resource:** [OWASP File Upload Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html)

---

### 🔹 **Exercise: Upload a Simple Payload and Achieve Remote Execution**  
**Goal:** Upload a crafted file and make the server execute something on your terms.

**Instructions:**  
- Use a vulnerable web app that allows unrestricted file uploads (e.g., DVWA or bWAPP).  
- Craft a small file that could act as an executable payload when accessed through the browser.  
- Upload the file and try to interact with it from the outside.  
- Can you make it run a command remotely? How do you verify it worked?
---


### 🔹 **Exercise: Evade File Upload Restrictions**  
**Goal:** Trick the upload filter into accepting a file that should be rejected.

**Instructions:**  
- Try uploading a potentially dangerous file, but the site blocks it.  
- Tweak it in subtle ways to sneak it past the filter.  
- Try renaming, changing metadata, or altering how the file is built.  
- Observe how the backend decides what’s “safe” and what isn’t.

---

### 🔖 **Project: Harden a Flask App Against Upload Exploits**  
**Goal:** Build a small Flask upload handler that defends itself against common bypasses.

**Instructions:**  
- Create a file uploader that accepts images and text files only.  
- Make sure your validation logic checks more than just the filename.  
- Store uploaded files in a way that prevents direct execution.  
- Test your own app by trying to upload something malicious—does it survive?

