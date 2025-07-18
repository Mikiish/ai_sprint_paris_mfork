;;;; secret_hash

(load (merge-pathnames "quicklisp/setup.lisp" (user-homedir-pathname)))
(with-output-to-string (*standard-output*)
  (ql:quickload '(:ironclad :babel :uiop :alexandria :cl-ppcre)))

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

(defun final-hash (user-input)
  "Compute SHA256(SHA256(token) ‖ user-input)."
  (let* ((token-hash (sha256-hex (getenv-or-fail "API_KEY")))
         (concat      (concatenate 'string token-hash user-input)))
    (sha256-hex concat)))

(defun main (&optional (user-input ""))
  "Main function to compute the final hash."
  (let ((result (final-hash user-input)))
    (format t "~a~%" result)))
;; Silent exit when run as script.
#+sbcl (main (uiop:getenv "USER_INPUT"))
;; ------------------------------------------------------------
;; End of script.
