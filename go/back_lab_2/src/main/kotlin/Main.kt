fun main(args: Array<String>) {
    println("Здравствуйте!")
    println("Вам доступны следующие команды:")

    println("1 — Создать фигуру \"Параллелограмм\";")
    println("2 — Выйти.")

    val answer = readln()

    if(answer == "2"){
        return
    }

    println("Задайте большее основание:")
    val bigSide = readln()

    println("Задайте меньшее основание:")
    val smallSide = readln()

    println("Задайте меньший угол:")
    val degree = readln()

    val parallelogram: IFigure = Parallelogram(
        bigSide = bigSide.toInt(),
        smallSide = smallSide.toInt(),
        degree = degree.toInt(),
    )
    var isContinue = true

    while (isContinue) {
        println("Выберите действие:")
        println("1 - Узнать площадь")
        println("2 - Узнать периметр")
        println("3 - Правильная ли фигура")
        println("4 - Выйти")

        val chosenFunc = readln()

        when(chosenFunc){
            "1" -> println("Площадь: ${parallelogram.calculateArea()}")
            "2" -> println("Периметр: ${parallelogram.calculatePerimeter()}")
            "3" -> {
                if(parallelogram.isShapeRight()){
                    println("Правильная")

                    return
                }

                println("Не правильная")
            }
            "4" -> isContinue = false
        }
    }
}