#lang racket
(define resta
  (lambda (p1 p2)
    (cond
      ((null? p1) p2)
      ((null? p2) p1)
      (else
       (cons (- (car p1) (car p2))
             (resta (cdr p1) (cdr p2)))))))
