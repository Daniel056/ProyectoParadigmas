#lang racket
;-----Proyecto #2 Paradigmas--------------------------------------
;-----Funciones con Polinomios------------------------------------
;-----Intengrantes: Esteban Montero Fonseca 304830405 Grupo 6pm---
;------------------ Jefferson Moreno Zuñiga 116270399 Grupo 3pm---
;------------------ Daniel Zamora García 402310604 Grupo 3pm------

;--------------------------------------------------------------------------
;Contruir el polinomio
(define display-p
  (lambda (polinomio)
    (cond
      ((null? polinomio) "")
      (else (cons-pol (simplifica polinomio) 0 "")))))

(define simplifica
  (lambda (polinomio)
    (cond
      ((null? polinomio) '())
      (else (simplifica1 (reverse polinomio))))))

(define simplifica1
  (lambda (polinomio)
    (cond
      ((null? polinomio) polinomio)
      ((= (car polinomio ) 0) (simplifica1 (cdr polinomio)))
      (else (reverse polinomio)))))

(define add
  (lambda (a b c d) 
    (string-append a (string-append (string-append b c) d))))

(define cons-pol
  (lambda (polinomio k resultado) 
    (cond
      ((null? polinomio) resultado)
      ((= (car polinomio) 0)
       (cond
         ((= k 0)
          (cond
            ((= (length polinomio) 1) (cons-pol (cdr polinomio) (+ k 1)(add resultado (number->string (car polinomio) "" ""))))
            (else (cons-pol (cdr polinomio) (+ k 1) resultado))))
         (else (cons-pol (cdr polinomio) (+ k 1) resultado))))
      ((> (car polinomio) 0)
       (cond
         ((= k 0) (cons-pol (cdr polinomio) (+ k 1) (add resultado (number->string (car polinomio)) "" "")))
         ((= k 1)
          (cond
            ((= (car polinomio) 1) (cons-pol (cdr polinomio) (+ k 1) (add resultado "+x" "" "")))
            (else (cons-pol (cdr polinomio) (+ k 1) (add resultado "+" (number->string (car polinomio)) "x")))))
         (else
          (cond
            ((= (car polinomio) 1) (cons-pol (cdr polinomio) (+ k 1) (add resultado "+x^" (number->string k) "")))
            (else
             (cons-pol (cdr polinomio) (+ k 1) (add resultado (add "+" (number->string (car polinomio)) "x^" (number->string k)) "" "")))))))
       (else
        (cond
          ((= k 0) (cons-pol (cdr polinomio) (+ k 1) (add resultado (number->string (car polinomio)) "" "")))
          ((= k 1)
           (cond
             ((= (car polinomio) -1) (cons-pol (cdr polinomio) (+ k 1) (add resultado "-x" "" "")))
             (else (cons-pol (cdr polinomio) (+ k 1) (add resultado (number->string (car polinomio)) "x" "")))))
          (else
           (cond
             ((= (car polinomio) -1) (cons-pol (cdr polinomio) (+ k 1) (add resultado "-x^" (number->string k) "")))
             (else (cons-pol (cdr polinomio) (+ k 1) (add resultado (number->string (car polinomio)) "x^" (number->string k)))))))))))

;--------------------------------------------------------------------------
;Suma de Polinomios
(define +p
  (lambda (polinomios)
    (cond
      ((null? polinomios) '())
      ((null? (cddr polinomios)) (display-p (suma (simplifica (car polinomios)) (simplifica (cadr polinomios)))))
      (else (+p (append (cddr polinomios) (cons (suma (simplifica (car polinomios)) (simplifica (cadr polinomios))) '())))))))

(define suma
  (lambda (p1 p2)
    (cond
      ((null? (simplifica p1)) (simplifica p2))
      ((null? (simplifica p2)) (simplifica p1))
      (else
       (cons (+ (car p1) (car p2))
             (suma (cdr p1) (cdr p2)))))))

;--------------------------------------------------------------------------
;Resta de Polinomios
(define -p
  (lambda (polinomios)
    (cond
      ((null? polinomios) '())
      ((null? (cddr polinomios)) (display-p (resta (simplifica (car polinomios)) (simplifica (cadr polinomios)))))
      (else (-p (append (cddr polinomios) (cons (resta (simplifica (car polinomios)) (simplifica (cadr polinomios))) '())))))))

(define resta
  (lambda (p1 p2)
    (cond
      ((null? (simplifica p1)) (simplifica p2))
      ((null? (simplifica p2)) (simplifica p1))
      (else
       (cons (- (car p1) (car p2))
             (resta (cdr p1) (cdr p2)))))))

;--------------------------------------------------------------------------
;Multiplicación de Polinomios
(define *p
  (lambda (polinomios)
    (cond
      ((null? polinomios) '())
      ((null? (cddr polinomios)) (display-p (multiplicacion (simplifica (car polinomios)) (simplifica (cadr polinomios)))))
      (else (*p (append (cddr polinomios) (cons (multiplicacion (simplifica (car polinomios)) (simplifica (cadr polinomios))) '())))))))

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
    (qt1 (simplifica p1) (simplifica p2) (simplifica p1) (simplifica p2) '())))

(define qt1
  (lambda (p1 p2 poli1 poli2 qt)
    (cond
      ((null? p1) (cond ((null? p2) qt) (else (append (cons poli1 '()) (cons poli2 '())))))
      ((null? p2) (cond ((null? p1) qt) (else (append (cons poli1 '()) (cons poli2 '())))))
      ((= (car p2) 0) (cond ((= (car p1) 0) (qt1 (cdr p1) (cdr p2))) (else (append (cons poli1 '()) (cons poli2 '())))))
      ((= (car p1) 0) (cond ((= (car p2) 0) (qt1 (cdr p1) (cdr p2))) (else (append (cons poli1 '()) (cons poli2 '())))))
      (else
       (qt1 (cdr p1) (cdr p2) poli1 poli2 (append qt (cons (quotient (car p1) (car p2)) '())))))))

;--------------------------------------------------------------------------
;División de Polinomios (Parte 2)
(define rem-p
  (lambda (p1 p2)
    (rem1 (simplifica p1) (simplifica p2) (simplifica p1) (simplifica p2) '())))

(define rem1
  (lambda (p1 p2 pol1 pol2 rm)
    (cond
      ((null? p1) (cond ((null? p2) rm) (else (append (cons pol1 '()) (cons pol2 '())))))
      ((null? p2) (cond ((null? p1) rm) (else (append (cons pol1 '()) (cons pol2 '())))))
      ((= (car p2) 0) (cond ((= (car p1) 0) (rem1 (cdr p1) (cdr p2))) (else (append (cons pol1 '()) (cons pol2 '())))))
      ((= (car p1) 0) (cond ((= (car p2) 0) (rem1 (cdr p1) (cdr p2))) (else (append (cons pol1 '()) (cons pol2 '())))))
      (else
       (rem1 (cdr p1) (cdr p2) pol1 pol2 (append rm (cons (remainder (car p1) (car p2)) '())))))))


;--------------------------------------------------------------------------
;División de Polinomios (Parte 3)
(define /-p
  (lambda (p1 p2)
    (div1 (simplifica p1) (simplifica p2))))

(define div1
  (lambda (p1 p2)
    (cond ((= (length (qt-p p1 p2)) 2) (qt-p p1 p2))
          (else (append (cons (qt-p p1 p2) '()) (cons (rem-p p1 p2) '()))))))

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
      (else (drv-p1 (cdr polinomios) (append (cons (deriva (simplifica (cdar polinomios)) '() 1) '()) derivadas))))))

(define deriva
  (lambda (polinomio derivada k)
    (cond
      ((null? polinomio) (simplifica derivada))
      (else
       (deriva (cdr polinomio) (append derivada (cons (* (car polinomio) k) '())) (+ k 1))))))


;--------------------------------------------------------------------------
;Evaluación de Polinomios
(define eval-p
  (lambda (polinomio x)
    (eval1 (simplifica polinomio) x)))


(define eval1
  (lambda (poly x)
    (cond 
      ((= (length poly) 0) 0)
      ((= (length poly) 1) (car poly))
      (else 
        (+ (car poly) (* x (eval1 (cdr poly) x)))))))


;--------------------------------------------------------------------------
;Factorización de Polinomios
(define divisores
  (lambda (num div k)
    (cond
      ((= num 0) div)
      ((> num 0)
       (cond ((= k 0) div)
         (else
          (cond ((= (remainder num k) 0) (divisores num (append div (cons k (cons (* -1 k) '()))) (- k 1)))
                (else (divisores num div (- k 1)))))))
      (else (divisores (* -1 num) div (* k -1))))))

(define divisores1
 (lambda (polinomio)
   (d (simplifica polinomio))))

(define d
  (lambda (polinomio)
   (cond
     ((null? polinomio) '())
     (else
      (cond
        ((= (car polinomio) 0) 0)
        (else
         (divisores (car polinomio) '() (car polinomio))))))))
;-------------------------------------------------------------------------
(define raices
  (lambda (pol divisores)
    (cond
      ((null? divisores) '())
      ((= (eval-p pol (car divisores)) 0) (append (cons 1 '()) (cons (* -1 (car divisores)) '())))
      (else
       (raices pol (cdr divisores))))))

(define raices1
  (lambda (polinomio)
    (r (simplifica polinomio))))

(define r
  (lambda (polinomio)
   (cond
    ((null? polinomio) '())
    (else
     (raices polinomio (divisores1 polinomio))))))
;--------------------------------------------------------------------------
(define ruffini
  (lambda (polinomio factor raiz)
    (cond
      ((null? polinomio) (list (reverse factor)))
      (else
       (cond
         ((= (+ (* raiz (car factor)) (car polinomio)) 0) factor)
         (else (ruffini (cdr polinomio) (append (cons (+ (* raiz (car factor)) (car polinomio)) '()) factor) raiz)))))))

(define ruffini1
  (lambda (polinomio)
    (ruff (simplifica polinomio))))

(define ruff
  (lambda (polinomio)
    (cond
      ((null? polinomio) '())
      (else
       (ruffini (cdr (reverse polinomio)) (cons (car (reverse polinomio)) '()) (* -1 (car (reverse (raices1 polinomio)))))))))
;--------------------------------------------------------------------------
(define factor
  (lambda (polinomio factores)
    (cond
      ((null? polinomio) factores)
      (else
       (append factores (cons (reverse (raices polinomio (divisores (car polinomio) '() (car polinomio))))
         (cons (ruffini (cdr (reverse polinomio))
               (cons (car (reverse polinomio)) '()) (* -1 (car (reverse (raices polinomio (divisores (car polinomio) '() (car polinomio))))))) '())))))))

(define factor1
  (lambda (polinomio factores)
    (cond
      ((null? polinomio) factores)
      ((= (length polinomio) 2) (factor1 '() (append (append factores '()) (cons polinomio '()))))
      (else
       (factor1 (ruffini1 polinomio) (append factores (cons (reverse (raices1 polinomio)) '())))))))

(define fact-p
  (lambda (polinomio)
    (cond
      ((null? polinomio) polinomio)
      (else
       (cond
         ((< (length (simplifica polinomio)) 3) (simplifica polinomio))
         ;((= 3 (length (simplifica polinomio))) (append (cons (cuadratica1 (simplifica polinomio)) '()) (cons (cuadratica2 (simplifica polinomio)) '())))  
         (else
          (factor1 (simplifica polinomio) '())))))))

(define cuadratica1
  (lambda (polinomio)
    (cond
      ((null? polinomio) polinomio)
      ((= 0 (car (reverse polinomio))) (simplifica polinomio))
      (else
       (cons (* -1 (/ (+ (* -1 (cadr polinomio)) (sqrt (- (* (cadr polinomio) (cadr polinomio)) (* 4 (* (car polinomio) (car (reverse polinomio)))))))
          (* 2 (car (reverse polinomio))))) '(1))))))

(define cuadratica2
  (lambda (polinomio)
    (cond
      ((null? polinomio) polinomio)
      ((= 0 (car (reverse polinomio))) '())
      (else
       (cons (* -1 (/ (- (* -1 (cadr polinomio)) (sqrt (- (* (cadr polinomio) (cadr polinomio)) (* 4 (* (car polinomio) (car (reverse polinomio)))))))
          (* 2 (car (reverse polinomio))))) '(1))))))
;--------------------------------------------------------------------------
(define common-f
  (lambda (polinomio cf)
    (cond
      ((null? polinomio) cf)
      ((= (length polinomio) 1) (gcd (car polinomio) cf))
      (else
       (common-f (cdr polinomio) (gcd (cadr polinomio) cf))))))

(define gcd
  (lambda (a b)
  (cond ((= b 0) a)
      (else (gcd b (modulo a b))))))

 






   
  
