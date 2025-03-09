window.checkFlag = async (encryptedBase64, keyStr) => {
  await sodium.ready;

  // Derive the key using Web Crypto's SHA‑256
  const keyBytes = sodium.from_string(keyStr);
  const hashBuffer = await crypto.subtle.digest("SHA-256", keyBytes);
  const hashedKey = new Uint8Array(hashBuffer);

  // Decode the base64 input into a Uint8Array
  const decoded = sodium.from_base64(encryptedBase64, sodium.base64_variants.ORIGINAL);

  // Extract nonce (first 12 bytes), tag (next 16 bytes), and ciphertext (rest)
  const nonce = decoded.slice(0, 12);
  const tag = decoded.slice(12, 28);
  const ciphertext = decoded.slice(28);

  // Libsodium expects the ciphertext to have the tag appended at the end.
  // Reassemble: [ciphertext || tag]
  const combined = new Uint8Array(ciphertext.length + tag.length);
  combined.set(ciphertext);
  combined.set(tag, ciphertext.length);

  try {
    // Decrypt the message.
    // Note: We pass `null` for additional data (AD) since none was used in encryption.
    const decrypted = sodium.crypto_aead_chacha20poly1305_ietf_decrypt(
      null,      // no additional data
      combined,  // ciphertext with tag appended
      null,      // no additional data
      nonce,     // nonce extracted from the beginning
      hashedKey  // key derived from SHA-256(keyStr)
    );

    // Convert decrypted bytes back to a string and return it.
    if (sodium.to_string(decrypted) === "This flag is correct!") {
      return true;
    }
  } catch (error) {
    return false;
  }
}
