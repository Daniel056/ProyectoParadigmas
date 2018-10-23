#lang racket
; polynomial functions
; NOTE: polynomials are represented inversely
; i.e. '(1 2 3) => 1 + 2x + 3x^2

; defunct
(define poly-to-string
  (lambda (poly)
    (letrec [(convert-to-strings
              (lambda (ls i)
                (if (null? ls)
                    '()
                    (cons
                     (cond [(= i 0) (if (> (car ls) 0)
                                        (string-append "+" (number->string (car ls)))
                                        (string-append "-" (number->string (- (car ls)))))]
                           [(= (car ls) 1) (string-append "+x^" (number->string i))]
                           [#t (string-append 
                                (if (> (car ls) 0)
                                    (string-append "+" (number->string (car ls)))
                                    (string-append "-" (number->string (- (car ls)))))
                                (if (= i 1)
                                    "x"
                                    (string-append "x^" (number->string i))))])
                     (convert-to-strings (cdr ls) (+ i 1))))))]
      (foldl string-append "" (convert-to-strings poly 0)))))
        