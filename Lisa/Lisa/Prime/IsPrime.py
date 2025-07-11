import random

def is_prime(n, k=40):
    """Test de primalité de Miller-Rabin avec k itérations (fiabilité élevée)."""
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False

    # Trouver d tel que n-1 = d * 2^r avec d impair
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    # Test de Miller-Rabin
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def hex_is_prime(hex_number):
    """Convertit un nombre hexadécimal en entier et teste sa primalité."""
    decimal_value = int(hex_number, 16)
    return is_prime(decimal_value)

if __name__ == "__main__":
    # Exemple d'utilisation avec des nombres en hexadécimal
    test_numbers = [
        "CAFFD366A99A307AE3B9860420B8F104AE39BA61361F5B05A42FE14EA984CC922A6D706E9C41BBE96246C38112B1521DD24E9554D069114F9FA8AEEE763614C247A8069AE40B9BE7CE0119A6EECAD6F01872F9A967F70417F20A22C6E8D2F039D5CB93F1D84BCF01B121A00F26CB5754263833DFBF043BF4A10243B771134B444BD77FF3355BB0AD7EC985D685FB34B9815A00AC2030CBD830E53AFFD21E6CDE01A995F8FC4C6E8F28D7EB54E980A51D2D721DD0106C0E18511E4CCB44B67B70F1A44A33369F00032DEDEDE570D54BAC9CC4397835D1168806BF7F79EC672023E1727E28978596694A4A8B38463F8AF10F3457A858539A2123385E3D3A564EDB36FF76AB1",
        "F883FDC831572F041B42F965C00E9C601646F2D1AC9810791B1BBBC61545B08F16D263302D9A9BC7C08BFD03CBC38B524813C26248114623B1E69C05C46366C9FD205828F598D9FB9F51B18B2DE5F331C62913F42BB36DC1A3CB1C58B2ABFE4CCD5E69E561203AF96F2DECBAC2E5EE9C7D41278FF2CF91BDEE80C775B116A2142C49AC2BC24EB5F08A6EBDD7A74EFA6F46D503FF74084F8E7C051D49438F817367AB11A46DD5D57C2C0D952E1337BAB66A88B87FA69F8C10A5BFB82F989FDA267588F8A503E3A5E3B4CE2A4843FEB3B930902A7598B4FCC8675D0C1E3D55BA093504491F97599D11F7CC356B1FD2A7EFE45707C26429A063A314DFB8BFB1F52C76B90641F"
    ]

    for hex_num in test_numbers:
        result = hex_is_prime(hex_num)
        print(f"Nombre hex: {hex_num[:10]}... est premier ? {result}")
