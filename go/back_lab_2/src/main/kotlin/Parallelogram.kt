import kotlin.math.sin

class Parallelogram(private val bigSide: Int, private val smallSide: Int, private val degree: Int) : IFigure {
    override fun isShapeRight(): Boolean {
        return bigSide == smallSide
    }

    override fun calculateArea(): Float {
        return bigSide * smallSide * sin(degree.toFloat())
    }

    override fun calculatePerimeter(): Int {
        return 2 * bigSide + 2 * smallSide
    }
}