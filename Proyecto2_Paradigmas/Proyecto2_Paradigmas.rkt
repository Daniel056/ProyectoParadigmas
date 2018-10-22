#lang racket
;-----Proyecto #2 Paradigmas------------------
;-----Funciones con Polinomios----------------
;-----Intengrantes: Esteban Montero Fonseca---
;------------------ Jefferson Moreno Zuñiga---
;------------------ Daniel Zamora García------

;Contruir el polinomio
(define display-p
  (lambda (L)
    (cond ((null? L)L)
          ((equal? 0 (car L)) display-p (cdr L))
          ((equal? 0 (car(cdr L)) display-p ((cons (car L) (cdr(cdr L))))))
          (else
           (quote 1)))))
          
  