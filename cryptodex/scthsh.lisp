;;;; secret_hash.lisp
;;;; ------------------------------------------------------------
;;;;  Reads the secret TOKEN from $API_TOKEN and computes
;;;;  SHA256(TOKEN).  No printing, no user interaction.
;;;;  Result is stored in *token-hash* for subsequent use.
;;;;
;;;;  Usage (inside SBCL):
;;;;      (load "secret_hash.lisp")
;;;;      *token-hash*
;;;;
;;;;  Or via --script : it exits silently (code 0) once the hash is ready.

(ql:quickload :ironclad)
(ql:quickload :uiop)

(in-package #:cl-user)

(defun getenv-or-fail (name)
  (or (uiop:getenv name)
      (progn
        (format *error-output* "[ERROR] Environment variable ~a is not set.~%" name)
        (uiop:quit 1))))

(defparameter +token+ (getenv-or-fail "API_TOKEN"))

(defun bytes->hex (seq)
  (with-output-to-string (s)
    (loop for b across seq do (format s "~2,'0x" b))))

(defun sha256-hex (string)
  (bytes->hex (ironclad:digest-sequence :sha256 (babel:string-to-octets string :encoding :utf-8))))

(defparameter *token-hash* (sha256-hex +token+))

;; Silent exit when run as script.
#+sbcl
(when (member :executable *features*)
  (uiop:quit 0))
