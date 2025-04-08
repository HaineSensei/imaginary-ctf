(defun get-flag ()
  (let ((flag 
          (or 
           ;; Try reading from environment variable
           #+sbcl (sb-ext:posix-getenv "FLAG")
           
           ;; Try reading from a file
           (handler-case 
               (with-open-file (stream "/flag" :direction :input)
                 (read-line stream nil nil))
             (error () nil))
           
           ;; Fallback message
           "Flag not found")))
    (format t "Flag: ~a~%" flag)
    flag))

(defun main ()
  (get-flag)
  (quit))

;; Ensure the main function is the entry point
(save-lisp-and-die "flag.core" :executable t :toplevel #'main)