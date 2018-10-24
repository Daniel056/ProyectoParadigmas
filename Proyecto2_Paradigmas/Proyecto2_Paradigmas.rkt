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
          
;--------------------------------------------------------------------------
;Suma de Polinomios
(define +p
  (lambda (p1 p2)
    (cond
      ((null? p1) p2)
      ((null? p2) p1)
      (else
       (cons (+ (car p1) (car p2))
             (+p (cdr p1) (cdr p2)))))))

;--------------------------------------------------------------------------
;Resta de Polinomios
(define -p
  (lambda (p1 p2)
    (cond
      ((null? p1) p2)
      ((null? p2) p1)
      (else
       (cons (- (car p1) (car p2))
             (-p (cdr p1) (cdr p2)))))))

;--------------------------------------------------------------------------
;Multiplicación de Polinomios


;--------------------------------------------------------------------------
;División de Polinomios (Parte 1)


;--------------------------------------------------------------------------
;Multiplicación de Polinomios (Parte 2)


;--------------------------------------------------------------------------
;División de Polinomios (Parte 3)


;--------------------------------------------------------------------------
;Derivación de Polinomios


;--------------------------------------------------------------------------
;Multiplicación de Polinomios


;--------------------------------------------------------------------------
;Evaluación de Polinomios
(define eval-p
  (lambda (poly x)
    (cond 
      ((= (length poly) 0) 0)
      ((= (length poly) 1) (car poly))
      (else 
        (+ (car poly) (* x (eval-p (cdr poly) x)))))))


;--------------------------------------------------------------------------
;Factorización de Polinomios
