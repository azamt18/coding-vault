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
            var sequentialMultiplier = new MatricesMultiplier();
            var parallelMultiplier = new MatricesMultiplierParallel();

            // warm-up to trigger JIT and ThreadPool initialization
            MeasureExecutionTicks(sequentialMultiplier, 10, iterations: 5);
            MeasureExecutionTicks(parallelMultiplier, 10, iterations: 5);

            // 1. Small matrix (3x3): Overhead of thread management makes sequential faster
            long smallSequentialTicks = MeasureExecutionTicks(sequentialMultiplier, 3, iterations: 100); // 0
            long smallParallelTicks = MeasureExecutionTicks(parallelMultiplier, 3, iterations: 100); // 4, 1

            // 2. Matrix (100x100): Sequential can still win due to low per-thread workload
            long largeSequentialTicks100 = MeasureExecutionTicks(sequentialMultiplier, 100, iterations: 3); // 45
            long largeParallelTicks100 = MeasureExecutionTicks(parallelMultiplier, 100, iterations: 3); // 131, 184
            Console.WriteLine($"{largeSequentialTicks100}, {largeParallelTicks100}");

            // 3. Matrix (150x150): Approaching crossover threshold
            long largeSequentialTicks150 = MeasureExecutionTicks(sequentialMultiplier, 150, iterations: 3); // 119
            long largeParallelTicks150 = MeasureExecutionTicks(parallelMultiplier, 150, iterations: 3); // 38, 19
            Console.WriteLine($"{largeSequentialTicks150}, {largeParallelTicks150}");

            // 4. Matrix (200x200): Parallel starts gaining advantage
            long largeSequentialTicks200 = MeasureExecutionTicks(sequentialMultiplier, 200, iterations: 3); // 293
            long largeParallelTicks200 = MeasureExecutionTicks(parallelMultiplier, 200, iterations: 3); // 42, 90
            Console.WriteLine($"{largeSequentialTicks200}, {largeParallelTicks200}");

            // 5. Matrix (206x206): Fine-tuning search near pivot area
            long largeSequentialTicks206 = MeasureExecutionTicks(sequentialMultiplier, 206, iterations: 3); // 304, 308
            long largeParallelTicks206 = MeasureExecutionTicks(parallelMultiplier, 206, iterations: 3); // 92, 47
            Console.WriteLine($"{largeSequentialTicks206}, {largeParallelTicks206}");

            // 6. Matrix (212x212): Fine-tuning search near pivot area
            long largeSequentialTicks212 = MeasureExecutionTicks(sequentialMultiplier, 212, iterations: 3); // 327
            long largeParallelTicks212 = MeasureExecutionTicks(parallelMultiplier, 212, iterations: 3); // 100, 51
            Console.WriteLine($"{largeSequentialTicks212}, {largeParallelTicks212}");

            // 7. Matrix (218x218): Fine-tuning search near pivot area
            long largeSequentialTicks218 = MeasureExecutionTicks(sequentialMultiplier, 218, iterations: 3); // 358
            long largeParallelTicks218 = MeasureExecutionTicks(parallelMultiplier, 218, iterations: 3); // 52
            Console.WriteLine($"{largeSequentialTicks218}, {largeParallelTicks218}");

            // 8. Matrix (225x225): Parallel workload variation
            long largeSequentialTicks225 = MeasureExecutionTicks(sequentialMultiplier, 225, iterations: 3); // 396
            long largeParallelTicks225 = MeasureExecutionTicks(parallelMultiplier, 225, iterations: 3); // 623, 546
            Console.WriteLine($"{largeSequentialTicks225}, {largeParallelTicks225}");

            // 9. Matrix (250x250): CPU-bound workload benefits from multi-core parallelization
            long largeSequentialTicks250 = MeasureExecutionTicks(sequentialMultiplier, 250, iterations: 3); // 558
            long largeParallelTicks250 = MeasureExecutionTicks(parallelMultiplier, 250, iterations: 3); // 132, 92
            Console.WriteLine($"{largeSequentialTicks250}, {largeParallelTicks250}");

            // Assertions:
            // - For small workloads, sequential has less overhead.
            // - For heavy workloads, parallel is faster.
            Assert.IsTrue(smallSequentialTicks <= smallParallelTicks,
                $"Expected sequential ({smallSequentialTicks} ticks) to be faster or equal to parallel ({smallParallelTicks} ticks) for 3x3 matrix.");

            Assert.IsTrue(largeParallelTicks250 < largeSequentialTicks250,
                $"Expected parallel ({largeParallelTicks250} ticks) to be faster than sequential ({largeSequentialTicks250} ticks) for 250x250 matrix.");

            // Note: Tried to find the pivot point where both approaches run at the same time.
            // Due to CPU spikes and OS thread scheduling, it is not realistic to expect
            // two execution times to land on the exact same ms/tick.
            
            // key takeaways
            // 1. evaluate complexity & operation cost of single operation
            // 2. test the crossover threshold for informed decision 
            
        }

        #region private methods

        long MeasureExecutionTicks(IMatricesMultiplier matrixMultiplier, int size, int iterations = 1)
        {
            var first = new Matrix(size, size, randomInit: true);
            var second = new Matrix(size, size, randomInit: true);

            var stopwatch = Stopwatch.StartNew();
            for (int i = 0; i < iterations; i++)
            {
                matrixMultiplier.Multiply(first, second);
            }
            stopwatch.Stop();

            return stopwatch.ElapsedMilliseconds;
        }

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
