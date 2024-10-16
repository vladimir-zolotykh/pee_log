(defun wclog-next ()
  "Create the next log file and add the date as the first line."
  (interactive)
  ;; Extract the current date from the first line of the current buffer
  (let* ((current-date-string (save-excursion
                                (goto-char (point-min))
                                (buffer-substring-no-properties (line-beginning-position) (line-end-position))))
         (current-date (date-to-time (concat current-date-string " 00:00:00")))
         (next-date (time-add current-date (days-to-time 1)))
         (next-date-string (format-time-string "%Y-%m-%d" next-date))
         (next-filename (concat next-date-string ".txt")))
    ;; Open the new file
    (find-file next-filename)
    ;; Insert the new date at the beginning
    (insert next-date-string "\n")
    ;; Save the new file
    (save-buffer)
    ;; Display success message
    (message "Created new file: %s" next-filename)))
