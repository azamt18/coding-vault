namespace MultiThreading.Task3.MatrixMultiplier.Matrices
{
    public interface IMatrix
    {
        #region properties

        long RowCount { get; }

        long ColCount { get; }

        #endregion

        #region methods

        void SetElement(long row, long col, long value);

        long GetElement(long row, long col);

        void Print();

        #endregion
    }
}