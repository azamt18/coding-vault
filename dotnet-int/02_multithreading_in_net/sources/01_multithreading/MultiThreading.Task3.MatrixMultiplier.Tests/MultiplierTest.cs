using System;
using System.Diagnostics;
using Microsoft.VisualStudio.TestTools.UnitTesting;
using MultiThreading.Task3.MatrixMultiplier.Matrices;
using MultiThreading.Task3.MatrixMultiplier.Multipliers;

namespace MultiThreading.Task3.MatrixMultiplier.Tests
{
    [TestClass]
    public class MultiplierTest
    {
        [TestMethod]
        public void MultiplyMatrix3On3Test()
        {
            TestMatrix3On3(new MatricesMultiplier());
            TestMatrix3On3(new MatricesMultiplierParallel());
        }

        [TestMethod]
        public void ParallelEfficiencyTest()
        {
            // todo: implement a test method to check the size of the matrix which makes parallel multiplication more effective than
            var stopwatch = new Stopwatch();
            
            // 100x100
            stopwatch.Start();
            TestMatrixNOnN(new MatricesMultiplierParallel(), 200, 200);
            var parallel200x200 = stopwatch.ElapsedMilliseconds;
            stopwatch.Restart();
            TestMatrixNOnN(new MatricesMultiplier(), 200, 200);
            var sequential200x200 = stopwatch.ElapsedMilliseconds;

            // 50x50
            stopwatch.Restart();
            TestMatrixNOnN(new MatricesMultiplierParallel(), 500, 500);
            var parallel500x500 = stopwatch.ElapsedMilliseconds;
            stopwatch.Restart();
            TestMatrixNOnN(new MatricesMultiplier(), 500, 500);
            var sequential500x500 = stopwatch.ElapsedMilliseconds;
            
            // 3x3
            stopwatch.Restart();
            TestMatrixNOnN(new MatricesMultiplierParallel(), 3, 3);
            var parallel3x3 = stopwatch.ElapsedMilliseconds;
            stopwatch.Restart();
            TestMatrixNOnN(new MatricesMultiplier(), 3, 3);
            var sequential3x3 = stopwatch.ElapsedMilliseconds;
            stopwatch.Stop();

            Assert.IsTrue(parallel200x200 < sequential200x200);
            Assert.IsTrue(parallel500x500 < sequential500x500);
            Assert.IsTrue(parallel3x3 >= sequential3x3);
        }

        #region private methods

        IMatrix TestMatrixNOnN(IMatricesMultiplier matrixMultiplier, int rows, int cols)
        {
            var first = new Matrix(rows, cols);
            var second = new Matrix(rows, cols);
            return matrixMultiplier.Multiply(first, second);
        }
        
        void TestMatrix3On3(IMatricesMultiplier matrixMultiplier)
        {
            if (matrixMultiplier == null)
            {
                throw new ArgumentNullException(nameof(matrixMultiplier));
            }

            var m1 = new Matrix(3, 3);
            m1.SetElement(0, 0, 34);
            m1.SetElement(0, 1, 2);
            m1.SetElement(0, 2, 6);

            m1.SetElement(1, 0, 5);
            m1.SetElement(1, 1, 4);
            m1.SetElement(1, 2, 54);

            m1.SetElement(2, 0, 2);
            m1.SetElement(2, 1, 9);
            m1.SetElement(2, 2, 8);

            var m2 = new Matrix(3, 3);
            m2.SetElement(0, 0, 12);
            m2.SetElement(0, 1, 52);
            m2.SetElement(0, 2, 85);

            m2.SetElement(1, 0, 5);
            m2.SetElement(1, 1, 5);
            m2.SetElement(1, 2, 54);

            m2.SetElement(2, 0, 5);
            m2.SetElement(2, 1, 8);
            m2.SetElement(2, 2, 9);

            var multiplied = matrixMultiplier.Multiply(m1, m2);
            Assert.AreEqual(448, multiplied.GetElement(0, 0));
            Assert.AreEqual(1826, multiplied.GetElement(0, 1));
            Assert.AreEqual(3052, multiplied.GetElement(0, 2));

            Assert.AreEqual(350, multiplied.GetElement(1, 0));
            Assert.AreEqual(712, multiplied.GetElement(1, 1));
            Assert.AreEqual(1127, multiplied.GetElement(1, 2));

            Assert.AreEqual(109, multiplied.GetElement(2, 0));
            Assert.AreEqual(213, multiplied.GetElement(2, 1));
            Assert.AreEqual(728, multiplied.GetElement(2, 2));
        }

        #endregion
    }
}
