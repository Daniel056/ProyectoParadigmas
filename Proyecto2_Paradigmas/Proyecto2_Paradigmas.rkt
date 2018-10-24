#lang racket
;-----Proyecto #2 Paradigmas------------------
;-----Funciones con Polinomios----------------
;-----Intengrantes: Esteban Montero Fonseca---
;------------------ Jefferson Moreno Zuñiga---
;------------------ Daniel Zamora García------

;Contruir el polinomio
; polynomial functions
; NOTE: polynomials are represented inversely
; i.e. '(1 2 3) => 1 + 2x + 3x^2

; defunct
(define display-p
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
