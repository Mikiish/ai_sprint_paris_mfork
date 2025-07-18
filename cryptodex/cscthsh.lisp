(load (merge-pathnames "quicklisp/setup.lisp"(user-homedir-pathname)))

(ql:quickload :ironclad)
(ql:quickload :uiop)

(in-package #:cl-user)

;; ------------------------------------------------------------
(defun getenv-or-fail (name)
  "Récupère la variable d’environnement NAME ou quitte avec erreur."
  (or (uiop:getenv name)
      (progn
        (format *error-output* "[ERROR] Environment variable ~a is not set.~%" name)
        (uiop:quit 1))))

;; ------------------------------------------------------------
(defun bytes->hex (seq)
  "Convert a (vector (unsigned-byte 8)) to lowercase hex string."
  (with-output-to-string (s)
    (loop for b across seq do (format s "~2,'0x" b))))

(defun sha256-hex (string)
  "Return SHA‑256 hex of STRING (UTF‑8)."
  (bytes->hex (ironclad:digest-sequence :sha256 (babel:string-to-octets string :encoding :utf-8))))

(defun main (&optional (user-input ""))
  "Main function to compute the final hash."
  (let ((result (sha256-hex user-input)))
    (format t "~a~%" result))) ; Silent exit when run as script.
#+sbcl (main (uiop:getenv "API_KEY"))
;; ------------------------------------------------------------
;; End of script.
