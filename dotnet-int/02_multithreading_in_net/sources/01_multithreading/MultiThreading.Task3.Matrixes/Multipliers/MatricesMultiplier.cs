using MultiThreading.Task3.MatrixMultiplier.Matrices;

namespace MultiThreading.Task3.MatrixMultiplier.Multipliers
{
    public class MatricesMultiplier : IMatricesMultiplier
    {
        public IMatrix Multiply(IMatrix m1, IMatrix m2)
        {
            var resultMatrix = new Matrix(m1.RowCount, m2.ColCount);
            for (long i = 0; i < m1.RowCount; i++)
            {
                for (byte j = 0; j < m2.ColCount; j++)
                {
                    long sum = 0;
                    for (byte k = 0; k < m1.ColCount; k++)
                    {
                        sum += m1.GetElement(i, k) * m2.GetElement(k, j);
                    }

                    resultMatrix.SetElement(i, j, sum);
                }
            }

            return resultMatrix;
        }
    }
}
