public class Solution {
    public int[] PlusOne(int[] digits) {

        string num = "";
        for(int i =0; i< digits.Length; i++){
            num = num+digits[i];
            
        }
        Console.WriteLine(num);
        var result = BigInteger.Parse(num);
        result += 1;
        num = result.ToString();

        Console.WriteLine(num);
        string[] strs = new string[num.Length];
        for(int i =0; i< num.Length; i++){
            strs[i] = num[i].ToString();
            
        }
        Console.WriteLine(String.Join(",", strs));

        int[] nums = Array.ConvertAll(strs, int.Parse);
        

        return nums;
    }
}