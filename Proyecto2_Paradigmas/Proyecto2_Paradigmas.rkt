#lang racket
;-----Proyecto #2 Paradigmas------------------
;-----Funciones con Polinomios----------------
;-----Intengrantes: Esteban Montero Fonseca---
;------------------ Jefferson Moreno Zuñiga---
;------------------ Daniel Zamora García------

;--------------------------------------------------------------------------
;Contruir el polinomio
(define display-p
  (lambda (polinomio)
    (cond
      ((null? polinomio) "")
      (else (cons-pol polinomio 0 "")))))

(define cons-pol
  (lambda (polinomio k resultado) 
    (cond
      ((null? polinomio) resultado)
      ((= (car polinomio) 0) (cons-pol (cdr polinomio) (+ k 1) resultado))
      ((> (car polinomio) 0)
       (cond
         ((= k 0) (cons-pol (cdr polinomio) (+ k 1) (string-append resultado (number->string (car polinomio)))))
         ((= k 1) (cons-pol (cdr polinomio) (+ k 1) (string-append resultado (string-append "+" (string-append (number->string (car polinomio)) "x")))))
         (else
          (cons-pol (cdr polinomio) (+ k 1)
                     (string-append resultado (string-append "+" (string-append (number->string (car polinomio)) (string-append "x^" (number->string k)))))))))
       (else
        (cond
          ((= k 0) (cons-pol (cdr polinomio) (+ k 1) (string-append resultado (number->string (car polinomio)))))
          ((= k 1) (cons-pol (cdr polinomio) (+ k 1) (string-append resultado (string-append (number->string (car polinomio)) "x"))))
          (else
           (cons-pol (cdr polinomio) (+ k 1)
                      (string-append resultado (string-append (number->string (car polinomio)) (string-append "x^" (number->string k)))))))))))

;--------------------------------------------------------------------------
;Suma de Polinomios
(define +p
  (lambda (polinomios)
    (cond
      ((null? polinomios) '())
      ((null? (cddr polinomios)) (display-p (suma (car polinomios) (cadr polinomios))))
      (else (+p (append (cddr polinomios) (cons (suma (car polinomios) (cadr polinomios)) '())))))))

(define suma
  (lambda (p1 p2)
    (cond
      ((null? p1) p2)
      ((null? p2) p1)
      (else
       (cons (+ (car p1) (car p2))
             (suma (cdr p1) (cdr p2)))))))

;--------------------------------------------------------------------------
;Resta de Polinomios
(define -p
  (lambda (polinomios)
    (cond
      ((null? polinomios) '())
      ((null? (cddr polinomios)) (display-p (resta (car polinomios) (cadr polinomios))))
      (else (-p (append (cddr polinomios) (cons (resta (car polinomios) (cadr polinomios)) '())))))))

(define resta
  (lambda (p1 p2)
    (cond
      ((null? p1) p2)
      ((null? p2) p1)
      (else
       (cons (- (car p1) (car p2))
             (resta (cdr p1) (cdr p2)))))))

;--------------------------------------------------------------------------
;Multiplicación de Polinomios
(define *p
  (lambda (polinomios)
    (cond
      ((null? polinomios) '())
      ((null? (cddr polinomios)) (display-p (multiplicacion (car polinomios) (cadr polinomios))))
      (else (*p (append (cddr polinomios) (cons (multiplicacion (car polinomios) (cadr polinomios)) '())))))))

(define multiplicacion
  (lambda (pol1 pol2)
    (cond
      ((null? pol2) '(0))
      (else
        (suma (multiplica pol1 (car pol2)) (multiplicacion (append '(0) pol1) (cdr pol2)))))))

(define multiplica
  (lambda (polinomio k)
    (cond
      ((null? polinomio) '())
      (else
       (cons (* k (car polinomio)) (multiplica (cdr polinomio) k))))))   

;--------------------------------------------------------------------------
;División de Polinomios (Parte 1)
(define qt-p
  (lambda (p1 p2)
    (cond
      ((null? p1) p2)
      ((null? p2) p1)
      ((= (car p2) 0) '(Division entre 0))
      (else
       (cons (quotient (car p1) (car p2))
             (qt-p (cdr p1) (cdr p2)))))))

;--------------------------------------------------------------------------
;División de Polinomios (Parte 2)
(define rem-p
  (lambda (p1 p2)
    (cond
      ((null? p1) p2)
      ((null? p2) p1)
      ((= (car p2) 0) '(Division entre 0))
      (else
       (cons (remainder (car p1) (car p2))
             (rem-p (cdr p1) (cdr p2)))))))


;--------------------------------------------------------------------------
;División de Polinomios (Parte 3)
(define /-p
  (lambda (p1 p2)
    (append (cons (qt-p p1 p2) '())
            (cons (rem-p p1 p2) '()))))

;--------------------------------------------------------------------------
;Derivación de Polinomios
(define drv-p
  (lambda (polinomios)
    (cond
      ((null? polinomios) '())
      (else
       (drv-p1 polinomios '())))))

(define drv-p1
  (lambda (polinomios derivadas)
    (cond
      ((null? polinomios) (reverse derivadas))
      (else (drv-p1 (cdr polinomios) (append (cons (deriva (cdar polinomios) '() 1) '()) derivadas))))))

(define deriva
  (lambda (polinomio derivada k)
    (cond
      ((null? polinomio) derivada)
      (else
       (deriva (cdr polinomio) (append derivada (cons (* (car polinomio) k) '())) (+ k 1))))))


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
